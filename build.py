#!/usr/bin/env python3
"""Build the static site: content.yaml + templates/ + static/ -> dist/.

Usage:
    python build.py            # build into dist/
    python build.py --serve    # build, then serve on http://localhost:8000
"""

import argparse
import datetime
import http.server
import shutil
import socketserver
from functools import partial
from pathlib import Path

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup

ROOT = Path(__file__).parent
OUT = ROOT / "dist"


def md(text, inline=False):
    html = markdown.markdown(text or "")
    if inline and html.startswith("<p>") and html.endswith("</p>") and html.count("<p>") == 1:
        html = html[3:-4]
    return Markup(html)


def build():
    content = yaml.safe_load((ROOT / "content.yaml").read_text(encoding="utf-8"))

    env = Environment(
        loader=FileSystemLoader(ROOT / "templates"),
        autoescape=select_autoescape(),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["md"] = md
    env.filters["md_inline"] = partial(md, inline=True)

    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "static", OUT)

    ctx = dict(content, updated=datetime.date.today().strftime("%B %Y"))
    (OUT / "index.html").write_text(env.get_template("index.html").render(ctx), encoding="utf-8")

    site_url = content["site"]["url"]
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"  <url><loc>{site_url}</loc><lastmod>{datetime.date.today()}</lastmod></url>\n"
        "</urlset>\n",
        encoding="utf-8",
    )
    print(f"Built {OUT}")


def serve(port):
    handler = partial(http.server.SimpleHTTPRequestHandler, directory=str(OUT))
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving on http://localhost:{port}")
        httpd.serve_forever()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--serve", action="store_true")
    ap.add_argument("--port", type=int, default=8000)
    args = ap.parse_args()
    build()
    if args.serve:
        serve(args.port)
