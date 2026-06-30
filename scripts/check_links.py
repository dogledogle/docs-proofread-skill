#!/usr/bin/env python3
"""Extract and check links from Markdown or HTML documentation."""

from __future__ import annotations

import argparse
import html.parser
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


DOC_EXTENSIONS = {".md", ".mdx", ".html", ".htm"}
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
REFERENCE_LINK_RE = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)", re.MULTILINE)


class HrefParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if key.lower() in {"href", "src"} and value:
                self.hrefs.append(value)


def iter_doc_files(targets: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw in targets:
        path = Path(raw).expanduser()
        if path.is_file() and path.suffix.lower() in DOC_EXTENSIONS:
            files.append(path)
        elif path.is_dir():
            files.extend(p for p in path.rglob("*") if p.is_file() and p.suffix.lower() in DOC_EXTENSIONS)
        else:
            print(f"WARNING: skipped missing or unsupported target: {raw}", file=sys.stderr)
    return sorted(set(files))


def extract_links(path: Path) -> list[dict[str, object]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    links: list[dict[str, object]] = []
    for match in MARKDOWN_LINK_RE.finditer(text):
        links.append({"file": str(path), "line": text.count("\n", 0, match.start()) + 1, "url": match.group(1)})
    for match in REFERENCE_LINK_RE.finditer(text):
        links.append({"file": str(path), "line": text.count("\n", 0, match.start()) + 1, "url": match.group(1)})
    parser = HrefParser()
    parser.feed(text)
    for href in parser.hrefs:
        line = find_line(text, href)
        links.append({"file": str(path), "line": line, "url": href})
    return links


def find_line(text: str, needle: str) -> int:
    index = text.find(needle)
    return text.count("\n", 0, index) + 1 if index >= 0 else 1


def split_link(url: str) -> tuple[str, str]:
    base, hash_mark, anchor = url.partition("#")
    return base, anchor if hash_mark else ""


def is_skippable(url: str) -> bool:
    parsed = urllib.parse.urlparse(url)
    return parsed.scheme in {"mailto", "tel", "javascript", "data"} or url.startswith("#")


def check_local(link: dict[str, object]) -> dict[str, object]:
    url = str(link["url"])
    base, _anchor = split_link(url)
    if not base:
        return {**link, "status": "skipped", "reason": "same-page anchor"}
    parsed = urllib.parse.urlparse(base)
    if parsed.scheme or base.startswith("//"):
        return {**link, "status": "skipped", "reason": "not local"}
    target = (Path(str(link["file"])).parent / urllib.parse.unquote(base)).resolve()
    if target.exists():
        return {**link, "status": "ok"}
    return {**link, "status": "broken", "reason": "local target missing", "target": str(target)}


def http_request(url: str, timeout: int) -> tuple[int, str]:
    for method in ("HEAD", "GET"):
        request = urllib.request.Request(url, method=method, headers={"User-Agent": "docs-proofreader/1.0"})
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return response.status, response.geturl()
        except urllib.error.HTTPError as exc:
            if method == "HEAD" and exc.code in {403, 405}:
                continue
            return exc.code, url
    return 0, url


def check_http(link: dict[str, object], timeout: int) -> dict[str, object]:
    url = str(link["url"])
    try:
        status, final_url = http_request(url, timeout)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return {**link, "status": "broken", "reason": str(exc)}
    if 200 <= status < 400:
        result = {**link, "status": "ok", "http_status": status}
        if final_url != url:
            result["final_url"] = final_url
        return result
    return {**link, "status": "broken", "reason": f"HTTP {status}", "http_status": status}


def check_link(link: dict[str, object], check_http_links: bool, timeout: int) -> dict[str, object]:
    url = str(link["url"])
    if is_skippable(url):
        return {**link, "status": "skipped", "reason": "unsupported or same-page scheme"}
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme in {"http", "https"}:
        if not check_http_links:
            return {**link, "status": "skipped", "reason": "http check disabled"}
        return check_http(link, timeout)
    return check_local(link)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("targets", nargs="+", help="Markdown/HTML files or directories to scan.")
    parser.add_argument("--check-http", action="store_true", help="Check HTTP(S) links with HEAD/GET.")
    parser.add_argument("--timeout", type=int, default=15, help="HTTP timeout in seconds.")
    parser.add_argument("--json", action="store_true", help="Emit JSON results.")
    args = parser.parse_args()

    links: list[dict[str, object]] = []
    for path in iter_doc_files(args.targets):
        links.extend(extract_links(path))
    results = [check_link(link, args.check_http, args.timeout) for link in links]

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for result in results:
            status = result["status"].upper()
            location = f"{result['file']}:{result['line']}"
            detail = f" - {result.get('reason')}" if result.get("reason") else ""
            print(f"{status}: {location} {result['url']}{detail}")

    return 1 if any(result["status"] == "broken" for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
