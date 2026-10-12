"""Check the actual Jekyll output, including URLs and unchanged historical PDFs."""
import argparse
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://mundo-marino-catamaranes.github.io/mundo-marino-catamaranes/"
HISTORICAL = {
    "Yo compenso.pdf": "233ea4823b946381b5ce84e5534966271bf868a20ea218257b38ad7ea9cbd9d0",
    "report_AROC_EstrellaFugaz_19062024.pdf": "1645df7ee22b50f79d147ac8e991800feb85c686e05b42fa187eec9e994ab38e",
    "report_AROC_Mascalzone_19062024.pdf": "bdb3dd3bbbed34399309bba4f3d42546e28733cd263d1b9da9b9a4ac93546e88",
    "report_AROC_MundoMarino2.pdf": "bc50f83528e491ba738155b3cd9f3ef5804498e132dd9db8828f87833803f6d4",
    "report_AROC_MundoMarino_19062024.pdf": "de91ec426474c33e0cd781f33c99be6b6fd7d523c1b40e138c8e8bb3443db27e",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


class Page(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.h1 = 0
        self.lang = None
        self.canonicals = []
        self.alternates = {}
        self.description = None
        self.links = []
        self.ids = set()
        self.jsonld = []
        self.capture = False
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "h1": self.h1 += 1
        if tag == "html": self.lang = attrs.get("lang")
        if attrs.get("id"): self.ids.add(attrs["id"])
        if tag == "meta" and attrs.get("name") == "description":
            self.description = attrs.get("content")
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonicals.append(attrs.get("href"))
        if tag == "link" and attrs.get("rel") == "alternate":
            self.alternates[attrs.get("hreflang")] = attrs.get("href")
        if tag == "a" and attrs.get("href"): self.links.append(attrs["href"])
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.capture = True
            self.jsonld.append("")

    def handle_data(self, data):
        if self.capture: self.jsonld[-1] += data

    def handle_endtag(self, tag):
        if tag == "script": self.capture = False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", type=Path)
    site = parser.parse_args().site.resolve()
    locations = ElementTree.parse(site / "sitemap.xml").findall(
        ".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
    require(len(locations) == 7, "Rendered sitemap must contain seven current pages")
    pages = {}
    for loc in locations:
        url = loc.text
        require(url.startswith(BASE), "Unexpected sitemap URL: " + url)
        path = site / (url[len(BASE):] or "index.html")
        html = path.read_text(encoding="utf-8")
        require("{{" not in html and "{%" not in html, "Unrendered Liquid: " + url)
        page = Page(html)
        pages[url] = page
        require(page.h1 == 1, "Expected one H1: " + url)
        require(page.lang == ("en" if url.endswith("README_en.html") else "es"), "Wrong language: " + url)
        require(page.canonicals == [url], "Wrong canonical: " + url)
        require(page.description, "Missing description: " + url)
        for value in page.jsonld: json.loads(value)
        for href in page.links:
            target_url = urlsplit(urljoin(url, href))
            if target_url.scheme not in ("http", "https") or target_url.netloc != urlsplit(BASE).netloc:
                continue
            prefix = urlsplit(BASE).path
            require(target_url.path.startswith(prefix), "Link escapes project path: " + href)
            require(not target_url.path.endswith(".md"), "Link opens raw Markdown instead of a page: " + href)
            target = site / (unquote(target_url.path[len(prefix):]) or "index.html")
            require(target.is_file(), f"Broken rendered link: {url} -> {href}")
            if target.suffix == ".html" and target_url.fragment:
                require(unquote(target_url.fragment) in Page(target.read_text(encoding="utf-8")).ids,
                        f"Missing fragment: {url} -> {href}")
    expected_alternates = {"es": BASE, "en": BASE + "README_en.html"}
    for url in expected_alternates.values():
        require(pages[url].alternates == expected_alternates, "Missing reciprocal hreflang: " + url)
    require(json.loads(pages[BASE].jsonld[0]) == json.loads((site / "company.json").read_text()),
            "Rendered organisation JSON-LD differs from company.json")
    for name, expected_hash in HISTORICAL.items():
        require(hashlib.sha256((site / name).read_bytes()).hexdigest() == expected_hash,
                "Historical PDF changed or missing: " + name)
    archive = (ROOT / "archivo/REFERENCIAS-2025.md").read_bytes()
    require(hashlib.sha1(b"blob " + str(len(archive)).encode() + b"\0" + archive).hexdigest()
            == "3b082e1bd11cbdcef34ae47c75b8708139f12a3f", "Historical references changed")
    require((site / "archivo/REFERENCIAS-2025.html").is_file(), "Historical references not rendered")
    print("OK: seven rendered pages, internal links, canonical, languages, JSON-LD and five unchanged historical PDFs.")


if __name__ == "__main__":
    main()
