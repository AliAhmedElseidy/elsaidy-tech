#!/usr/bin/env python3
"""Validate the static bilingual site with Python's standard library."""
from __future__ import annotations
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET
import sys

ROOT = Path(__file__).resolve().parents[1] / "site"
DOMAIN = "https://tech.elsaidy.org"

class Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.meta = {}
        self.links = []
        self.lang = ""
        self.h1_count = 0
        self._in_title = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang", "")
        elif tag == "title":
            self._in_title = True
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "link":
            self.links.append(a)
        elif tag == "meta":
            name = a.get("name") or a.get("property")
            if name:
                self.meta[name] = a.get("content", "")
        elif tag == "a" and "href" in a:
            self.links.append(a)
    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
    def handle_data(self, data):
        if self._in_title:
            self.title += data

def run() -> int:
    errors = []
    pages = sorted(ROOT.rglob("index.html"))
    actual_urls = set()
    if not pages:
        print("No generated pages found")
        return 1
    for path in pages:
        route = "/" + str(path.relative_to(ROOT).parent).replace("\\", "/").strip(".")
        if route == "/":
            route = "/"
        elif not route.endswith("/"):
            route += "/"
        full_url = DOMAIN + route
        actual_urls.add(full_url)
        html = path.read_text(encoding="utf-8")
        if "erpnext" in html.lower():
            errors.append(f"{path.relative_to(ROOT)}: legacy vendor name in public copy")
        doc = Page()
        doc.feed(html)
        canonical = [x.get("href") for x in doc.links if x.get("rel") == "canonical"]
        alternates = {x.get("hreflang"): x.get("href") for x in doc.links if x.get("rel") == "alternate" and x.get("hreflang")}
        expected_lang = "en" if route.startswith("/en/") else "ar"
        for test, msg in [
            (doc.lang == expected_lang, "wrong html lang"),
            (doc.h1_count == 1, "expected one h1"),
            (len(doc.title.strip()) >= 12, "missing page title"),
            (len(doc.meta.get("description", "")) >= 40, "missing description"),
            (canonical == [full_url], "missing or incorrect canonical"),
            (alternates.get("ar") and alternates.get("en"), "missing bilingual alternate"),
            (doc.meta.get("og:title") and doc.meta.get("og:image"), "missing social metadata"),
            ("undefined" not in html and "lorem ipsum" not in html.lower(), "placeholder text found"),
        ]:
            if not test:
                errors.append(f"{path.relative_to(ROOT)}: {msg}")
        for item in doc.links:
            href = item.get("href", "")
            if not href.startswith("/") or href.startswith("//"):
                continue
            parsed = urlsplit(href)
            local = unquote(parsed.path).lstrip("/")
            if not local or local.endswith("/"):
                local = local + "index.html"
            if not (ROOT / local).is_file():
                errors.append(f"{path.relative_to(ROOT)}: broken internal link {href}")
    xml_path = ROOT / "sitemap.xml"
    if not xml_path.exists():
        errors.append("missing sitemap.xml")
    else:
        try:
            tree = ET.parse(xml_path)
            listed = {node.text for node in tree.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")}
            if listed != actual_urls:
                errors.append(f"sitemap mismatch: expected {len(actual_urls)}, got {len(listed)}")
        except ET.ParseError as exc:
            errors.append(f"invalid sitemap XML: {exc}")
    for required in ["assets/styles.css", "assets/favicon.svg", "robots.txt", "_headers", "404.html"]:
        if not (ROOT / required).is_file():
            errors.append("missing " + required)
    if errors:
        print("SITE CHECK FAILED")
        for error in errors:
            print(" - " + error)
        return 1
    print(f"SITE CHECK PASSED: {len(pages)} pages, bilingual metadata, canonical URLs, sitemap and internal links")
    return 0

if __name__ == "__main__":
    sys.exit(run())
