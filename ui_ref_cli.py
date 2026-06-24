#!/usr/bin/env python3
"""Local UI reference research CLI.

Index local UI reference images, and optionally collect explicitly listed
external UI reference pages — caching HTML plus link/gallery metadata — for
design research. Collection is intentionally conservative:

- local references are indexed first
- external URLs are fetched only when explicitly listed
- assets are not downloaded unless requested
- a politeness delay, per-run page cap, and robots.txt checks are built in
"""

from __future__ import annotations

import argparse
import json
import os
import re
import struct
import sys
import time
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse
from urllib import request, robotparser, error


IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
VIDEO_EXTS = {".mp4", ".webm", ".mov", ".m4v"}
HTML_EXTS = {".html", ".htm"}
MEDIA_EXTS = IMAGE_EXTS | VIDEO_EXTS | HTML_EXTS
MAX_DOWNLOAD_BYTES = 25 * 1024 * 1024
__version__ = "0.3.0"

DEFAULT_CONFIG = {
    "project_name": "",
    "local_refs": "references/ui",
    "workspace": "ui_research",
    "urls_file": "ui_research/urls.txt",
    "default_delay_seconds": 8.0,
    "default_max_pages": 20,
    "user_agent": "ui-ref-cli/0.2 (+https://github.com/SillyToolValley/Game-UI-Reference-Cli)",
    "gallery_class": "galleryimage",
}

CONFIG_SEARCH_PATHS = (
    "ui_ref_config.json",
    "ui_research/ui_ref_config.json",
    "docs/ui_research/ui_ref_config.json",
)

# Known UI-reference databases and how to read them.
#
# To add a site, append one entry. `match` is a domain substring used to auto-select the
# preset from a URL. `mode` is "gallery" (structured anchors, like Game UI Database) or
# "images" (harvest the rendered page's <img>/srcset images — the generic default). For
# "gallery" mode, `gallery_class` is the anchor class that marks a gallery image; its
# title/id/thumbnail are read from data-title / data-imageid / data-thumb (see LinkExtractor).
#
# Login-walled sites (e.g. Mobbin's app screens) are intentionally NOT listed: their
# galleries require authentication and cannot be collected by this tool.
SITE_PRESETS: dict[str, dict[str, str]] = {
    "gameuidatabase":  {"match": "gameuidatabase.com", "mode": "gallery", "gallery_class": "galleryimage", "notes": "Game UI Database — structured gallery; JS-rendered, use --browser."},
    "interfaceingame": {"match": "interfaceingame.com", "mode": "images", "notes": "Interface In Game — game UI screenshots."},
    "screenlane":      {"match": "screenlane.com", "mode": "images", "notes": "Mobile UI/UX flows."},
    "collectui":       {"match": "collectui.com", "mode": "images", "notes": "Daily UI inspiration."},
    "landbook":        {"match": "land-book.com", "mode": "images", "notes": "Landing-page gallery."},
    "lapaninja":       {"match": "lapa.ninja", "mode": "images", "notes": "Landing-page examples."},
    "refero":          {"match": "refero.design", "mode": "images", "notes": "Web/iOS UI inspiration."},
    "dribbble":        {"match": "dribbble.com", "mode": "images", "notes": "Design shots (public pages)."},
    "behance":         {"match": "behance.net", "mode": "images", "notes": "Creative showcase (public pages)."},
}

DEFAULT_GALLERY_CLASS = "galleryimage"

# A realistic desktop browser UA for the --browser (Playwright) path. Many sites serve
# different markup to — or block — the default "HeadlessChrome" UA, so present a normal one.
BROWSER_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"


def find_preset(url: str, site: str | None) -> dict[str, str] | None:
    if site and site in SITE_PRESETS:
        return SITE_PRESETS[site]
    host = urlparse(url).netloc.lower()
    for preset in SITE_PRESETS.values():
        if preset["match"] in host:
            return preset
    return None


def resolve_gallery_class(url: str, explicit: str | None, site: str | None, cfg: dict[str, Any]) -> str:
    if explicit:
        return explicit
    preset = find_preset(url, site)
    if preset and preset.get("gallery_class"):
        return preset["gallery_class"]
    return cfg.get("gallery_class", DEFAULT_GALLERY_CLASS)


def resolve_mode(url: str, explicit_mode: str | None, explicit_gallery_class: str | None, site: str | None) -> str:
    """Return 'gallery' (structured anchor extraction) or 'images' (generic harvest of the
    rendered page's images). Precedence: --mode > site preset > 'gallery' if a gallery class
    was given, else 'images'."""
    if explicit_mode:
        return explicit_mode
    preset = find_preset(url, site)
    if preset and preset.get("mode"):
        return preset["mode"]
    return "gallery" if explicit_gallery_class else "images"

# Generic UI/game-screen tag heuristics, inferred from a reference's folder path.
TAG_RULES = {
    "hud": ["hud", "overlay", "vitals", "minimap", "marker", "waypoint", "prompt", "counter", "notification"],
    "combat": ["combat", "battle", "action", "ability", "skill-use", "attack", "boss"],
    "progression": ["reward", "result", "level-complete", "unlocked", "progress", "skill-tree"],
    "inventory": ["inventory", "item", "equip", "craft", "trading", "buying", "resource", "stats"],
    "navigation": ["title", "settings", "option", "menu", "save", "difficulty", "load"],
    "narrative": ["dialog", "speech", "story", "cutscene", "codex", "journal", "inbox", "outbox"],
    "tutorial": ["tutorial", "guided", "modal-info"],
    "party": ["party", "players", "character-select", "class"],
    "mission": ["mission", "objective", "quest"],
}


@dataclass
class HtmlFetchResult:
    url: str
    status: int | str
    content_type: str
    html: str
    fetched_at: str
    error: str = ""


class LinkExtractor(HTMLParser):
    def __init__(self, base_url: str, gallery_class: str = "galleryimage") -> None:
        super().__init__()
        self.base_url = base_url
        self.gallery_class = gallery_class
        self.links: list[dict[str, str]] = []
        self.assets: list[dict[str, str]] = []
        self.gallery_items: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {k.lower(): (v if v is not None else "") for k, v in attrs}
        if tag == "a" and attr.get("href"):
            href = urljoin(self.base_url, attr["href"])
            self.links.append({"tag": tag, "attr": "href", "url": href})
            if is_media_url(href):
                self.assets.append({"tag": tag, "attr": "href", "url": href})
            if self.gallery_class in attr.get("class", "").split():
                item = {
                    "image_url": href,
                    "title": clean_html_text(attr.get("data-title", "")),
                    "image_id": attr["data-imageid"] if "data-imageid" in attr and attr["data-imageid"] else attr.get("id", ""),
                    "image_index": attr.get("data-imageindex", ""),
                    "size": attr.get("data-size", ""),
                }
                if attr.get("data-thumb"):
                    item["thumb_url"] = urljoin(self.base_url, attr["data-thumb"])
                    self.assets.append({"tag": tag, "attr": "data-thumb", "url": item["thumb_url"]})
                if attr.get("data-customthumb"):
                    item["custom_thumb_url"] = urljoin(self.base_url, attr["data-customthumb"])
                    self.assets.append({"tag": tag, "attr": "data-customthumb", "url": item["custom_thumb_url"]})
                self.gallery_items.append({k: v for k, v in item.items() if v})
        if tag in {"img", "video", "source"}:
            alt = clean_html_text(attr.get("alt", "")) or clean_html_text(attr.get("title", ""))
            for key in ("src", "data-src", "data-original", "data-lazy-src"):
                if attr.get(key):
                    self.assets.append({"tag": tag, "attr": key, "url": urljoin(self.base_url, attr[key]), "alt": alt})
            if attr.get("srcset"):
                for raw_part in attr["srcset"].split(","):
                    candidate = raw_part.strip().split(" ")[0]
                    if candidate:
                        self.assets.append({"tag": tag, "attr": "srcset", "url": urljoin(self.base_url, candidate), "alt": alt})


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")


def is_media_url(url: str) -> bool:
    suffix = Path(urlparse(url).path.lower()).suffix
    return suffix in MEDIA_EXTS


def clean_html_text(raw: str) -> str:
    text = unescape(raw or "")
    text = re.sub(r"<[^>]+>", " ", text)
    return " ".join(text.split())


def read_text(path: Path) -> str:
    for enc in ("utf-8-sig", "utf-8", "cp949", "utf-16"):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")


def load_json(path: Path) -> Any:
    return json.loads(read_text(path))


def rel_to_root(root: Path, path: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve())).replace("\\", "/")
    except ValueError:
        try:
            return os.path.relpath(str(path.resolve()), str(root.resolve())).replace("\\", "/")
        except ValueError:
            return str(path).replace("\\", "/")


def resolve_under_root(root: Path, value: str) -> Path:
    candidate = Path(value)
    return candidate.resolve() if candidate.is_absolute() else (root / candidate).resolve()


def safe_slug(text: str, fallback: str = "item") -> str:
    # Keep ASCII alphanumerics plus Unicode word characters (letters/digits in any
    # language), so non-Latin titles still produce readable, filesystem-safe slugs.
    text = re.sub(r"https?://", "", text.strip().lower())
    text = re.sub(r"[^\w.-]+", "-", text, flags=re.UNICODE)
    text = text.strip("-._")
    return text[:100] or fallback


def project_root_from_args(args: argparse.Namespace) -> Path:
    return Path(args.project_root).resolve()


def config_path(root: Path, args: argparse.Namespace) -> Path:
    if getattr(args, "config", None):
        return Path(args.config).resolve()
    return root / "ui_ref_config.json"


def discover_config_path(root: Path, args: argparse.Namespace) -> Path:
    if getattr(args, "config", None):
        return Path(args.config).resolve()
    for rel_path in CONFIG_SEARCH_PATHS:
        candidate = root / rel_path
        if candidate.exists():
            return candidate
    return config_path(root, args)


def default_urls_file(workspace: str) -> str:
    cleaned = workspace.replace("\\", "/").rstrip("/")
    return f"{cleaned}/urls.txt"


def config_slash_path(value: Any) -> str:
    return str(value).replace("\\", "/")


def default_config(root: Path | None = None) -> dict[str, Any]:
    cfg = dict(DEFAULT_CONFIG)
    if root and not cfg["project_name"]:
        cfg["project_name"] = root.name
    return cfg


def load_config(root: Path, args: argparse.Namespace, required: bool = False) -> dict[str, Any]:
    path = discover_config_path(root, args)
    if path.exists():
        cfg = default_config(root)
        cfg.update(load_json(path))
        return cfg
    if required:
        raise SystemExit(f"Config not found: {path}. Run `ui-ref init` first.")
    return default_config(root)


def cfg_path(root: Path, cfg: dict[str, Any], key: str) -> Path:
    return (root / cfg[key]).resolve()


def image_dimensions(path: Path) -> tuple[int, int] | None:
    suffix = path.suffix.lower()
    try:
        with path.open("rb") as f:
            if suffix == ".png":
                header = f.read(24)
                if header.startswith(b"\x89PNG\r\n\x1a\n") and len(header) >= 24:
                    width, height = struct.unpack(">II", header[16:24])
                    return int(width), int(height)
            if suffix == ".gif":
                header = f.read(10)
                if header[:6] in (b"GIF87a", b"GIF89a") and len(header) >= 10:
                    width, height = struct.unpack("<HH", header[6:10])
                    return int(width), int(height)
            if suffix in {".jpg", ".jpeg"}:
                if f.read(2) != b"\xff\xd8":
                    return None
                while True:
                    byte = f.read(1)
                    if not byte:
                        return None
                    if byte != b"\xff":
                        continue
                    marker = f.read(1)
                    while marker == b"\xff":
                        marker = f.read(1)
                    raw_len = f.read(2)
                    if len(raw_len) != 2:
                        return None
                    seg_len = struct.unpack(">H", raw_len)[0]
                    if seg_len < 2:
                        return None
                    if marker in {b"\xc0", b"\xc1", b"\xc2", b"\xc3", b"\xc5", b"\xc6", b"\xc7", b"\xc9", b"\xca", b"\xcb", b"\xcd", b"\xce", b"\xcf"}:
                        data = f.read(seg_len - 2)
                        if len(data) >= 5:
                            height, width = struct.unpack(">HH", data[1:5])
                            return int(width), int(height)
                    else:
                        f.seek(seg_len - 2, 1)
    except (OSError, struct.error, ValueError):
        return None
    return None


def infer_tags(text: str) -> list[str]:
    lower = text.lower().replace("\\", "/")
    tags: set[str] = set()
    for tag, needles in TAG_RULES.items():
        if any(needle in lower for needle in needles):
            tags.add(tag)
    return sorted(tags)


def summarize_items(items: list[dict[str, Any]]) -> dict[str, Any]:
    by_collection = Counter(item["collection"] for item in items)
    by_category = Counter(item["category"] for item in items)
    by_type = Counter(item["media_type"] for item in items)
    by_tag: Counter[str] = Counter()
    for item in items:
        by_tag.update(item.get("tags", []))
    return {
        "total_items": len(items),
        "by_collection": dict(by_collection.most_common()),
        "by_category": dict(by_category.most_common()),
        "by_media_type": dict(by_type.most_common()),
        "by_tag": dict(by_tag.most_common()),
    }


def manifest_markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# UI Reference Manifest",
        "",
        f"Generated: {manifest['generated_at']}",
        f"Source type: `{manifest.get('source_type', 'local_scan')}`",
        f"Root: `{manifest['local_refs']}`",
        "",
        "This manifest is produced by `ui-ref scan-local`. It indexes files that already exist under "
        "the local references directory. It is not evidence that those files were fetched from an "
        "external website by `ui-ref collect`.",
        "",
        "## Summary",
        "",
    ]
    summary = manifest["summary"]
    lines.append(f"- Total items: {summary['total_items']}")
    for key in ("by_collection", "by_category", "by_media_type", "by_tag"):
        lines.append(f"- {key}: " + ", ".join(f"{k}={v}" for k, v in summary[key].items()))
    lines.extend(["", "## Items", ""])
    for item in manifest["items"]:
        tags = ", ".join(item["tags"]) or "untagged"
        dims = f"{item['width']}x{item['height']}" if item.get("width") and item.get("height") else "unknown"
        lines.append(f"- `{item['path']}` | {item['collection']} / {item['category']} | {item['media_type']} | {dims} | {tags}")
    return "\n".join(lines) + "\n"


def command_init(args: argparse.Namespace) -> int:
    root = project_root_from_args(args)
    cfg = default_config(root)
    if args.project_name:
        cfg["project_name"] = args.project_name
    if args.local_refs:
        cfg["local_refs"] = config_slash_path(args.local_refs)
    if args.workspace:
        cfg["workspace"] = config_slash_path(args.workspace)
        if not args.urls_file:
            cfg["urls_file"] = default_urls_file(cfg["workspace"])
    if args.urls_file:
        cfg["urls_file"] = config_slash_path(args.urls_file)
    cfg_path_value = config_path(root, args)
    existing_config = discover_config_path(root, args)
    if existing_config.exists() and existing_config.resolve() != cfg_path_value.resolve():
        print(f"Warning: existing config at {existing_config} will be shadowed by {cfg_path_value}")
    workspace = cfg_path(root, cfg, "workspace")
    for folder in ("cache/html", "cache/assets", "manifests"):
        (workspace / folder).mkdir(parents=True, exist_ok=True)
    refs_dir = cfg_path(root, cfg, "local_refs")
    refs_dir.mkdir(parents=True, exist_ok=True)
    urls_file = cfg_path(root, cfg, "urls_file")
    if not urls_file.exists():
        write_text(
            urls_file,
            "# Add one explicit reference URL per line.\n"
            "# Keep runs small and slow. Assets are not downloaded unless requested.\n"
            "# Example (a JS-rendered gallery needs `--browser`):\n"
            "# https://www.gameuidatabase.com/index.php?&set=1&scrn=904\n",
        )
    write_json(cfg_path_value, cfg)
    print(f"Initialized UI research workspace: {workspace}")
    print(f"Config: {cfg_path_value}")
    print(f"Local references folder: {refs_dir}")
    print(f"URL list: {urls_file}")
    return 0


def command_scan_local(args: argparse.Namespace) -> int:
    root = project_root_from_args(args)
    cfg = load_config(root, args)
    refs_root = cfg_path(root, cfg, "local_refs")
    workspace = cfg_path(root, cfg, "workspace")
    if not refs_root.exists():
        raise SystemExit(f"Local references directory not found: {refs_root}")

    items: list[dict[str, Any]] = []
    for path in sorted(refs_root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in MEDIA_EXTS:
            continue
        rel = path.relative_to(refs_root)
        parts = rel.parts
        collection = parts[0] if len(parts) >= 2 else "uncategorized"
        category = parts[1] if len(parts) >= 3 else "uncategorized"
        suffix = path.suffix.lower()
        media_type = "image" if suffix in IMAGE_EXTS else "video" if suffix in VIDEO_EXTS else "html"
        dims = image_dimensions(path) if media_type == "image" else None
        item = {
            "path": rel_to_root(root, path),
            "collection": collection,
            "category": category,
            "filename": path.name,
            "media_type": media_type,
            "extension": suffix,
            "size_bytes": path.stat().st_size,
            "tags": infer_tags(str(rel)),
        }
        if dims:
            item["width"], item["height"] = dims
        items.append(item)

    manifest = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "source_type": "local_scan",
        "tool_command": "scan-local",
        "local_refs": rel_to_root(root, refs_root),
        "summary": summarize_items(items),
        "items": items,
    }
    out_json = workspace / "manifests" / "local_ui_refs_manifest.json"
    out_md = workspace / "manifests" / "local_ui_refs_manifest.md"
    write_json(out_json, manifest)
    write_text(out_md, manifest_markdown(manifest))
    print(f"Indexed {len(items)} local UI reference files.")
    print(f"Manifest: {out_json}")
    print(f"Summary: {out_md}")
    return 0


def can_fetch_url(url: str, user_agent: str, timeout: float = 10.0) -> tuple[bool, str]:
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return False, f"unsupported-scheme:{parsed.scheme or 'none'}"
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp = robotparser.RobotFileParser()
    rp.set_url(robots_url)
    try:
        with request.urlopen(request.Request(robots_url, headers={"User-Agent": user_agent}), timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
        rp.parse(raw.splitlines())
    except error.HTTPError as exc:
        if exc.code in (401, 403):
            return False, "robots-forbidden"
        return True, "robots-unavailable"
    except Exception:
        return True, "robots-unavailable"
    try:
        return bool(rp.can_fetch(user_agent, url)), robots_url
    except Exception:
        return True, "robots-parse-failed"


def fetch_static(url: str, user_agent: str, timeout: float) -> HtmlFetchResult:
    req = request.Request(url, headers={"User-Agent": user_agent, "Accept": "text/html,application/xhtml+xml"})
    fetched_at = datetime.now().isoformat(timespec="seconds")
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read(MAX_DOWNLOAD_BYTES + 1)
            if len(raw) > MAX_DOWNLOAD_BYTES:
                return HtmlFetchResult(url, resp.status, resp.headers.get("content-type", ""), "", fetched_at,
                                       f"response exceeds {MAX_DOWNLOAD_BYTES} bytes; skipped")
            charset = resp.headers.get_content_charset() or "utf-8"
            html = raw.decode(charset, errors="replace")
            return HtmlFetchResult(url, resp.status, resp.headers.get("content-type", ""), html, fetched_at)
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
        return HtmlFetchResult(url, exc.code, exc.headers.get("content-type", ""), body, fetched_at, str(exc))
    except Exception as exc:
        return HtmlFetchResult(url, "ERROR", "", "", fetched_at, f"{type(exc).__name__}: {exc}")


def fetch_browser(url: str, timeout_ms: int, wait_ms: int, headless: bool, scroll: int = 0, user_agent: str = BROWSER_UA) -> HtmlFetchResult:
    """Render a JS page with a headless browser (Playwright) and return the final HTML.
    Optionally scroll to trigger lazy-loaded images. Used only by `collect --browser`."""
    fetched_at = datetime.now().isoformat(timespec="seconds")
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
    except Exception as exc:
        return HtmlFetchResult(url, "ERROR", "", "", fetched_at,
                               f"Playwright unavailable ({exc}). Install with: "
                               f"pip install 'ui-ref-cli[browser]' && playwright install chromium")
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=headless)
            try:
                context = browser.new_context(user_agent=user_agent, viewport={"width": 1366, "height": 900}, locale="en-US")
                page = context.new_page()
                response = page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
                status = response.status if response else "OK"
                content_type = (response.headers.get("content-type", "") if response else "") or "text/html"
                try:
                    page.wait_for_load_state("networkidle", timeout=min(timeout_ms, 12000))
                except Exception:
                    pass
                if wait_ms > 0:
                    page.wait_for_timeout(wait_ms)
                for _ in range(max(0, scroll)):
                    page.mouse.wheel(0, 24000)
                    page.wait_for_timeout(900)
                html = page.content()
                return HtmlFetchResult(url, status, content_type, html, fetched_at)
            finally:
                browser.close()
    except Exception as exc:
        return HtmlFetchResult(url, "ERROR", "", "", fetched_at, f"{type(exc).__name__}: {exc}")


def load_urls(path: Path, explicit_urls: list[str] | None) -> list[str]:
    urls: list[str] = []
    if path.exists():
        for line in read_text(path).splitlines():
            cleaned = line.strip()
            if cleaned and not cleaned.startswith("#"):
                urls.append(cleaned)
    if explicit_urls:
        urls.extend(explicit_urls)
    deduped: list[str] = []
    seen: set[str] = set()
    for url in urls:
        if url not in seen:
            deduped.append(url)
            seen.add(url)
    return deduped


def extract_page_title(html: str) -> str:
    match = re.search(r"<title[^>]*>(.*?)</title>", html, flags=re.IGNORECASE | re.DOTALL)
    return clean_html_text(match.group(1)) if match else ""


def extract_links(html: str, base_url: str, gallery_class: str = "galleryimage") -> dict[str, Any]:
    parser = LinkExtractor(base_url, gallery_class=gallery_class)
    parser.feed(html)
    return {
        "title": extract_page_title(html),
        "links": parser.links,
        "assets": parser.assets,
        "gallery_items": parser.gallery_items,
    }


def harvest_image_items(assets: list[dict[str, str]]) -> list[dict[str, str]]:
    """Generic image harvest for sites without a structured gallery: turn the rendered
    page's <img>/srcset image assets into gallery-style items for download and the
    contact sheet. Obvious chrome (icons, avatars, logos, sprites) is filtered out."""
    items: list[dict[str, str]] = []
    seen: set[str] = set()
    skip_tokens = ("sprite", "favicon", "/icon", "icons/", "avatar", "logo", "placeholder", "blank.")
    for asset in assets:
        url = asset.get("url", "")
        if not url or url in seen or url.startswith("data:"):
            continue
        suffix = Path(urlparse(url).path.lower()).suffix
        looks_image = suffix in IMAGE_EXTS or asset.get("tag") in ("img", "source") or asset.get("attr") == "srcset"
        if not looks_image:
            continue
        if any(token in url.lower() for token in skip_tokens):
            continue
        seen.add(url)
        item: dict[str, str] = {"image_url": url, "thumb_url": url}
        if asset.get("alt"):
            item["title"] = asset["alt"]
        items.append(item)
    return items


def downloaded_filename(page_index: int, item_index: int, url: str) -> str:
    suffix = Path(urlparse(url).path).suffix.lower()
    if suffix not in IMAGE_EXTS:
        suffix = ".bin"
    return f"{page_index:03d}_{item_index:02d}_{safe_slug(Path(urlparse(url).path).stem, 'asset')}{suffix}"


def download_binary(url: str, destination: Path, user_agent: str, timeout: float, referer: str) -> dict[str, Any]:
    if urlparse(url).scheme not in ("http", "https"):
        return {"status": "SKIPPED", "content_type": "", "bytes": 0, "error": f"unsupported scheme: {urlparse(url).scheme or 'none'}"}
    req = request.Request(
        url,
        headers={
            "User-Agent": user_agent,
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            "Referer": referer,
        },
    )
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            content_type = resp.headers.get("content-type", "")
            raw = resp.read(MAX_DOWNLOAD_BYTES + 1)
            if len(raw) > MAX_DOWNLOAD_BYTES:
                return {"status": resp.status, "content_type": content_type, "bytes": 0, "error": f"exceeds {MAX_DOWNLOAD_BYTES} byte limit"}
            if content_type.lower().startswith(("text/", "application/xhtml", "application/json")):
                return {"status": resp.status, "content_type": content_type, "bytes": 0, "error": f"non-image content-type: {content_type}"}
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(raw)
            return {
                "status": resp.status,
                "content_type": content_type,
                "bytes": len(raw),
                "error": "",
            }
    except error.HTTPError as exc:
        return {
            "status": exc.code,
            "content_type": exc.headers.get("content-type", "") if exc.headers else "",
            "bytes": 0,
            "error": str(exc),
        }
    except Exception as exc:
        return {
            "status": "ERROR",
            "content_type": "",
            "bytes": 0,
            "error": f"{type(exc).__name__}: {exc}",
        }


def download_gallery_assets(
    root: Path,
    record: dict[str, Any],
    assets_root: Path,
    user_agent: str,
    timeout: float,
    limit: int,
    use_full_images: bool,
    title_filters: list[str] | None = None,
    gallery_source: list[dict[str, Any]] | None = None,
) -> None:
    downloaded: list[dict[str, Any]] = []
    seen: set[str] = set()
    page_index = int(record.get("index", 0))
    lowered_filters = [value.lower() for value in title_filters or [] if value.strip()]
    gallery_items = list(gallery_source if gallery_source is not None else record.get("gallery_items", []))
    if lowered_filters:
        ordered: list[dict[str, str]] = []
        ordered_seen: set[str] = set()
        for title_filter in lowered_filters:
            for candidate in gallery_items:
                title = candidate.get("title", "")
                candidate_key = candidate.get("image_url") or candidate.get("thumb_url") or str(candidate)
                if candidate_key in ordered_seen or title_filter not in title.lower():
                    continue
                ordered.append(candidate)
                ordered_seen.add(candidate_key)
        gallery_items = ordered
    for item in gallery_items:
        url = item.get("image_url") if use_full_images else item.get("thumb_url") or item.get("image_url")
        if not url or url in seen:
            continue
        seen.add(url)
        if urlparse(url).scheme not in ("http", "https"):
            continue
        # Allow image extensions and extension-less CDN URLs; reject clearly non-image
        # extensions (.html/.css/.js/...). download_binary's content-type check is the backstop.
        suffix = Path(urlparse(url).path.lower()).suffix
        if suffix and suffix not in IMAGE_EXTS:
            continue
        local_path = assets_root / downloaded_filename(page_index, len(downloaded) + 1, url)
        result = download_binary(url, local_path, user_agent, timeout, referer=record.get("url", ""))
        downloaded.append(
            {
                "source_url": url,
                "local_path": rel_to_root(root, local_path),
                "title": item.get("title", ""),
                "size": item.get("size", ""),
                "image_id": item.get("image_id", ""),
                **result,
            }
        )
        if len(downloaded) >= limit:
            break
    record["downloaded_assets"] = downloaded


def _esc(text: Any) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def write_contact_sheet(out_path: Path, run_id: str, records: list[dict[str, Any]], root: Path) -> int:
    """Write a browsable HTML contact sheet of what a collect run gathered.

    Downloaded thumbnails render inline (local files); the full gallery listing is a
    table of title/size/source links. Remote thumbnails are intentionally not inlined
    because many sites block hotlinking (so they would not load from a local file).
    """
    cards: list[str] = []
    rows: list[str] = []
    for record in records:
        for asset in record.get("downloaded_assets", []):
            if asset.get("error"):
                continue
            local = asset.get("local_path", "")
            abs_local = (root / local).resolve() if local else None
            src_attr = ""
            if abs_local and abs_local.exists():
                try:
                    src_attr = os.path.relpath(abs_local, out_path.parent).replace("\\", "/")
                except ValueError:
                    src_attr = str(abs_local)
            caption = asset.get("title", "") or Path(local).name
            cards.append(
                f'<figure><img loading="lazy" src="{_esc(src_attr)}" alt="{_esc(caption)}"/>'
                f'<figcaption>{_esc(caption)}<br><a href="{_esc(asset.get("source_url", ""))}">source</a>'
                f'{(" · " + _esc(asset.get("size", ""))) if asset.get("size") else ""}</figcaption></figure>'
            )
        for gallery in record.get("gallery_items", []):
            rows.append(
                "<tr>"
                f'<td>{_esc(gallery.get("title", ""))}</td>'
                f'<td>{_esc(gallery.get("size", ""))}</td>'
                f'<td><a href="{_esc(gallery.get("image_url", ""))}">image</a></td>'
                "</tr>"
            )
    body_cards = "".join(cards) or "<p>No assets downloaded — re-run with <code>--download-gallery-assets</code>.</p>"
    body_rows = "".join(rows) or "<tr><td colspan=\"3\">No gallery items extracted (try <code>--browser</code>).</td></tr>"
    html = (
        "<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
        f"<title>ui-ref contact sheet {_esc(run_id)}</title>\n"
        "<style>"
        "body{font-family:system-ui,Arial,sans-serif;background:#17131f;color:#ead9b9;margin:24px}"
        "h1,h2{color:#f2c14e} a{color:#7ad7d9}"
        ".grid{display:flex;flex-wrap:wrap;gap:14px}"
        "figure{margin:0;width:220px;background:#221a2d;border:1px solid #6b4a37;border-radius:10px;padding:8px}"
        "figure img{width:100%;height:auto;border-radius:6px;background:#2a2035}"
        "figcaption{font-size:12px;margin-top:6px;word-break:break-word}"
        "table{border-collapse:collapse;width:100%;margin-top:8px}"
        "td,th{border-bottom:1px solid #3a2f44;padding:6px;font-size:13px;text-align:left}"
        "</style></head><body>\n"
        f"<h1>UI reference contact sheet — run {_esc(run_id)}</h1>\n"
        f"<p>Pages: {len(records)} · downloaded thumbnails: {len(cards)} · gallery items: {len(rows)}. "
        "Open this file in a browser.</p>\n"
        f"<h2>Downloaded thumbnails</h2>\n<div class=\"grid\">{body_cards}</div>\n"
        f"<h2>All gallery items ({len(rows)})</h2>\n"
        f"<table><tr><th>title</th><th>size</th><th>link</th></tr>{body_rows}</table>\n"
        "</body></html>\n"
    )
    write_text(out_path, html)
    return len(cards)


def command_collect(args: argparse.Namespace) -> int:
    root = project_root_from_args(args)
    cfg = load_config(root, args)
    workspace = cfg_path(root, cfg, "workspace")
    urls_file = resolve_under_root(root, args.urls_file) if args.urls_file else cfg_path(root, cfg, "urls_file")
    urls = load_urls(urls_file, args.url)
    if not urls:
        raise SystemExit(f"No URLs found. Add URLs to {urls_file} or pass --url.")

    user_agent = args.user_agent or cfg["user_agent"]
    max_pages = args.max_pages if args.max_pages is not None else int(cfg["default_max_pages"])
    delay = args.delay if args.delay is not None else float(cfg["default_delay_seconds"])
    timeout = float(args.timeout)
    selected = urls[:max_pages]
    run_id = now_stamp()
    run_dir = workspace / "cache" / "html" / run_id
    assets_dir = workspace / "cache" / "assets" / run_id
    records: list[dict[str, Any]] = []

    print(f"Collecting {len(selected)} page(s), delay={delay}s, browser={args.browser}")
    for index, url in enumerate(selected, start=1):
        allowed, robots_note = can_fetch_url(url, user_agent)
        record: dict[str, Any] = {
            "index": index,
            "url": url,
            "robots": robots_note,
            "allowed_by_robots": allowed,
            "fetched_at": datetime.now().isoformat(timespec="seconds"),
        }
        if not allowed:
            record["status"] = "SKIPPED"
            record["error"] = f"not fetched ({robots_note})"
            records.append(record)
            print(f"[{index}/{len(selected)}] skipped ({robots_note}): {url}")
        else:
            print(f"[{index}/{len(selected)}] fetching: {url}")
            if args.browser:
                result = fetch_browser(url, timeout_ms=int(timeout * 1000), wait_ms=int(args.wait), headless=not args.no_headless, scroll=args.scroll, user_agent=BROWSER_UA)
            else:
                result = fetch_static(url, user_agent=user_agent, timeout=timeout)
            record["status"] = result.status
            record["content_type"] = result.content_type
            record["error"] = result.error
            if result.html:
                parsed = urlparse(url)
                html_name = f"{index:03d}_{safe_slug(parsed.netloc + parsed.path, 'page')}.html"
                html_path = run_dir / html_name
                write_text(html_path, result.html)
                gallery_class = resolve_gallery_class(url, args.gallery_class, args.site, cfg)
                extracted = extract_links(result.html, url, gallery_class=gallery_class)
                if resolve_mode(url, args.mode, args.gallery_class, args.site) == "images" and not extracted["gallery_items"]:
                    extracted["gallery_items"] = harvest_image_items(extracted["assets"])
                record["html_path"] = rel_to_root(root, html_path)
                record["page_title"] = extracted["title"]
                record["link_count"] = len(extracted["links"])
                record["asset_count"] = len(extracted["assets"])
                record["gallery_count"] = len(extracted["gallery_items"])
                record["links"] = extracted["links"][: args.keep_links]
                record["assets"] = extracted["assets"][: args.keep_assets]
                record["gallery_items"] = extracted["gallery_items"][: args.keep_gallery]
                if args.download_gallery_assets:
                    download_gallery_assets(
                        root=root,
                        record=record,
                        assets_root=assets_dir,
                        user_agent=user_agent,
                        timeout=timeout,
                        limit=args.download_asset_limit,
                        use_full_images=args.download_full_images,
                        title_filters=args.download_title_contains,
                        gallery_source=extracted["gallery_items"],
                    )
            records.append(record)
        if index < len(selected) and delay > 0:
            time.sleep(delay)

    manifest = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "source_type": "external_collect",
        "tool_command": "collect",
        "run_id": run_id,
        "source_urls_file": rel_to_root(root, urls_file),
        "records": records,
    }
    out_path = workspace / "manifests" / f"collected_pages_{run_id}.json"
    write_json(out_path, manifest)
    print(f"Collection manifest: {out_path}")

    sheet_path = workspace / "manifests" / f"contact_sheet_{run_id}.html"
    shown = write_contact_sheet(sheet_path, run_id, records, root)
    print(f"Contact sheet: {sheet_path} ({shown} thumbnail(s))")

    total_gallery = sum(int(r.get("gallery_count", 0)) for r in records)
    any_html = any(r.get("html_path") for r in records)
    if not args.browser and total_gallery == 0 and any_html:
        print(
            "Tip: 0 items were extracted with the static fetcher. Most reference sites are "
            "JavaScript-rendered — re-run with --browser (needs: pip install 'ui-ref-cli[browser]' "
            "&& playwright install chromium). For a structured gallery, set --gallery-class; "
            "for a generic image harvest, use --mode images."
        )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ui-ref", description="Local UI reference research CLI.")
    parser.add_argument("--version", action="version", version=f"ui-ref {__version__}")
    parser.add_argument("--project-root", default=".", help="Project root. Default: current directory.")
    parser.add_argument("--config", default=None, help="Path to ui_ref_config.json.")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create the UI research workspace and config.")
    init.add_argument("--project-name", default=None, help="Project display name.")
    init.add_argument("--local-refs", default=None, help="Local UI reference folder. Default: references/ui.")
    init.add_argument("--workspace", default=None, help="UI research workspace. Default: ui_research.")
    init.add_argument("--urls-file", default=None, help="URL list path. Default: <workspace>/urls.txt.")
    init.set_defaults(func=command_init)

    scan = sub.add_parser("scan-local", help="Index local UI reference files into a manifest.")
    scan.set_defaults(func=command_scan_local)

    collect = sub.add_parser("collect", help="Fetch explicitly listed reference pages slowly and cache HTML/link metadata.")
    collect.add_argument("--urls-file", default=None, help="URL list file. Default: config urls_file.")
    collect.add_argument("--url", action="append", help="Explicit URL to collect. Can be repeated.")
    collect.add_argument("--max-pages", type=int, default=None, help="Max pages in this run.")
    collect.add_argument("--delay", type=float, default=None, help="Delay between pages in seconds.")
    collect.add_argument("--timeout", type=float, default=30.0, help="Network timeout in seconds.")
    collect.add_argument("--user-agent", default=None, help="User-Agent for static fetches and robots checks.")
    collect.add_argument("--site", default=None, choices=sorted(SITE_PRESETS), help="Force a known site preset (else auto-detected from each URL's domain).")
    collect.add_argument("--mode", default=None, choices=["gallery", "images"], help="Extraction mode: 'gallery' (structured anchors) or 'images' (harvest page images). Default: per-site preset, else images.")
    collect.add_argument("--gallery-class", default=None, help="Override the gallery anchor class for gallery mode (default: per-site preset, else galleryimage).")
    collect.add_argument("--browser", action="store_true", help="Render JS pages with a headless browser (Playwright). Needs the [browser] extra.")
    collect.add_argument("--wait", type=int, default=3000, help="Browser wait after load in milliseconds.")
    collect.add_argument("--scroll", type=int, default=4, help="In --browser mode, scroll N times to load lazy images (default 4).")
    collect.add_argument("--no-headless", action="store_true", help="Show browser window when --browser is used.")
    collect.add_argument("--keep-links", type=int, default=200, help="Max link records to keep per page.")
    collect.add_argument("--keep-assets", type=int, default=200, help="Max asset records to keep per page.")
    collect.add_argument("--keep-gallery", type=int, default=100, help="Max gallery image records to keep per page.")
    collect.add_argument("--download-gallery-assets", action="store_true", help="Download a small number of gallery images per page.")
    collect.add_argument("--download-asset-limit", type=int, default=3, help="Max gallery images to download per page.")
    collect.add_argument("--download-full-images", action="store_true", help="Download full gallery images instead of thumbnails.")
    collect.add_argument("--download-title-contains", action="append", default=[], help="Only download gallery images whose title contains this text (items without a title are excluded). Can be repeated.")
    collect.set_defaults(func=command_collect)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
