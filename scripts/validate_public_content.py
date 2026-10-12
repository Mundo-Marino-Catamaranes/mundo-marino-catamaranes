"""Offline consistency checks; this does not certify external links or permits."""
import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://mundo-marino-catamaranes.github.io/mundo-marino-catamaranes/"

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.lang = None
        self.capture = False
        self.jsonld = ""
        self.canonical = None
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "h1": self.h1 += 1
        if tag == "html": self.lang = attrs.get("lang")
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = attrs.get("href")
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.capture = True
    def handle_endtag(self, tag):
        if tag == "script": self.capture = False
    def handle_data(self, data):
        if self.capture: self.jsonld += data

def require(condition, message):
    if not condition: raise ValueError(message)

def main():
    for path in ROOT.glob("*.json"):
        json.loads(path.read_text(encoding="utf-8"))
    company = json.loads((ROOT / "company.json").read_text(encoding="utf-8"))
    require(company["@type"] == "Organization", "Incorrect organisation type")
    require(company["@id"] == "https://mundomarino.es/#organization", "Identity drift")
    es = json.loads((ROOT / "mundo-marino.json").read_text(encoding="utf-8"))
    en = json.loads((ROOT / "mundo-marino-en.json").read_text(encoding="utf-8"))
    ports = [p["name"] for p in company["areaServed"]]
    require(ports == es["puertos"] == en["ports"], "Destination mismatch")
    require(es["empresa"]["cif"] == en["company"]["tax_id"] == company["taxID"], "Tax ID mismatch")
    routes = json.loads((ROOT / "routes.json").read_text(encoding="utf-8"))["routes"]
    require(len(routes) == 6, "Expected six reviewed routes")
    require(len({r["id"] for r in routes}) == len(routes), "Duplicate route IDs")
    require(sum(r["destination"] == "Almería" for r in routes) == 4, "Almería catalogue mismatch")
    for route in routes:
        require(urlsplit(route["official_url"]).netloc == "mundomarino.es", "Non-official product URL")
        require(route["live_availability_verified"] is False, "Unsupported inventory claim")
    page = Page()
    page.feed((ROOT / "index.html").read_text(encoding="utf-8"))
    require(page.h1 == 1 and page.lang == "es", "Main page H1/language issue")
    require(page.canonical == BASE, "Incorrect canonical URL")
    require(json.loads(page.jsonld) == company, "Embedded JSON-LD differs from company.json")
    sitemap = ElementTree.parse(ROOT / "sitemap.xml")
    locations = sitemap.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
    require(len(locations) == 7, "Expected seven sitemap pages in the correct XML namespace")
    require(len({loc.text for loc in locations}) == len(locations), "Duplicate sitemap URLs")
    for loc in locations:
        require(loc.text.startswith(BASE), "Sitemap contains a different host/path")
        path = loc.text[len(BASE):] or "index.html"
        target = ROOT / path
        require(target.exists() or (target.suffix == ".html" and target.with_suffix(".md").exists()), "Missing sitemap target: " + path)
    for doc in ROOT.glob("*.md"):
        for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", doc.read_text(encoding="utf-8")):
            if urlsplit(link).scheme or link.startswith("#"): continue
            target = ROOT / unquote(link.split("#")[0])
            require(target.exists(), f"Broken local link in {doc.name}: {link}")
    subprocess.run([sys.executable, str(ROOT / "scripts/generate_readme.py"), "--check"], check=True)
    print("OK: JSON, identity, six routes, local links, HTML and sitemap. External availability not tested.")

if __name__ == "__main__":
    main()
