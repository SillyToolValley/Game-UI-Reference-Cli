#!/usr/bin/env python3
"""Render a UX/UI 디자인 문서 (markdown) to a wide landscape PDF (+ HTML).

Markdown stays the editable source; this produces the shareable deliverable in the
format design teams expect (16:9 landscape, wide tables that don't wrap to mush).

    pip install markdown
    python build_pdf.py design.md                 # -> design.html + design.pdf next to it
    python build_pdf.py design.md --css design-pdf.css --out out/design.pdf

Needs a headless Chrome or Edge (ships with Windows). The HTML is written next to the
source so relative image/SVG paths (wireframes/*.svg, references/ui/*.jpg) resolve.
"""
import argparse, os, re, shutil, subprocess, sys

CHROME_CANDIDATES = [
    r"C:/Program Files/Google/Chrome/Application/chrome.exe",
    r"C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
    r"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
    r"C:/Program Files/Microsoft/Edge/Application/msedge.exe",
    "google-chrome", "chromium", "chrome", "msedge",
]

def find_chrome():
    for c in CHROME_CANDIDATES:
        if os.path.sep in c or "/" in c:
            if os.path.exists(c): return c
        elif shutil.which(c): return shutil.which(c)
    return None

def md_to_html(md_text):
    # task-list checkboxes -> symbols (python-markdown has no built-in tasklist)
    md_text = re.sub(r'^(\s*[-*]\s+)\[ \]\s', r'\1☐ ', md_text, flags=re.M)
    md_text = re.sub(r'^(\s*[-*]\s+)\[[xX]\]\s', r'\1☑ ', md_text, flags=re.M)
    import markdown
    html = markdown.markdown(md_text, extensions=['tables', 'fenced_code', 'attr_list', 'sane_lists'])
    # per-screen section (### 5.x) starts a new page
    html = re.sub(r'<h3>(\s*5\.\d)', r'<h3 class="screen-break">\1', html)
    # tag the big legend/state tables (optional hook for finer CSS)
    return html

def _rewrite_paths(html, reldir):
    # prefix relative img src so an appended page's images resolve from the main doc's dir
    if not reldir or reldir == ".":
        return html
    return re.sub(r'(<img\b[^>]*\bsrc=")(?!https?:|/|file:)([^"]+)"',
                  lambda m: f'{m.group(1)}{reldir}/{m.group(2)}"', html)

def build(md_path, css_path, out_pdf, appends=None):
    md_path = os.path.abspath(md_path)
    out_pdf = os.path.abspath(out_pdf)
    src_dir = os.path.dirname(md_path)
    title = os.path.splitext(os.path.basename(md_path))[0]
    css = open(css_path, encoding='utf-8').read() if css_path and os.path.exists(css_path) else ""
    body = md_to_html(open(md_path, encoding='utf-8').read())
    # append reference pages (etc.) as a self-contained appendix in the shared PDF
    for ap in (appends or []):
        ap = os.path.abspath(ap)
        if not os.path.exists(ap):
            print("  (skip append, not found):", ap); continue
        reldir = os.path.relpath(os.path.dirname(ap), src_dir).replace(os.sep, '/')
        ap_html = _rewrite_paths(md_to_html(open(ap, encoding='utf-8').read()), reldir)
        body += '<div style="break-before:page"></div>\n' + ap_html
    html_path = os.path.join(src_dir, title + ".html")
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write('<!doctype html><html lang="ko"><head><meta charset="utf-8">'
                f'<title>{title}</title><style>{css}</style></head><body>{body}</body></html>')
    print("HTML:", html_path)

    chrome = find_chrome()
    if not chrome:
        print("No Chrome/Edge found — HTML written; open it and Print-to-PDF (landscape) manually.")
        return html_path, None
    if os.path.exists(out_pdf):
        os.remove(out_pdf)
    cmd = [chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
           f"--print-to-pdf={out_pdf}", "file:///" + html_path.replace('\\', '/')]
    subprocess.run(cmd, check=False, capture_output=True)
    if os.path.exists(out_pdf):
        print("PDF :", out_pdf, f"({os.path.getsize(out_pdf)//1024} KB)")
    else:
        print("PDF generation failed; HTML is available at", html_path)
    return html_path, out_pdf

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("md")
    ap.add_argument("--css", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "design-pdf.css"))
    ap.add_argument("--out", default=None)
    ap.add_argument("--append", action="append", default=[],
                    help="Extra markdown to append as an appendix (e.g. reference pages); repeatable.")
    a = ap.parse_args()
    out = a.out or os.path.splitext(os.path.abspath(a.md))[0] + ".pdf"
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    build(a.md, a.css, out, appends=a.append)
