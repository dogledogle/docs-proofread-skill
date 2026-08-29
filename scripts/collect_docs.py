#!/usr/bin/env python3
"""Collect local documentation files or fetch URL text snapshots."""

from __future__ import annotations

import argparse
import fnmatch
import html.parser
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


DEFAULT_EXTENSIONS = {
    ".md",
    ".mdx",
    ".rst",
    ".txt",
    ".html",
    ".htm",
    ".vue",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
}


class TextExtractor(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._skip = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript"}:
            self._skip += 1
        if tag in {"p", "div", "section", "article", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6"}:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript"} and self._skip:
            self._skip -= 1
        if tag in {"p", "div", "section", "article", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6"}:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self._skip:
            text = " ".join(data.split())
            if text:
                self.parts.append(text)

    def text(self) -> str:
        lines = [" ".join(line.split()) for line in "".join(self.parts).splitlines()]
        return "\n".join(line for line in lines if line)


def is_url(value: str) -> bool:
    parsed = urllib.parse.urlparse(value)
    return parsed.scheme in {"http", "https"}


def parse_extensions(values: list[str] | None) -> set[str]:
    if not values:
        return DEFAULT_EXTENSIONS
    result: set[str] = set()
    for value in values:
        for item in value.split(","):
            item = item.strip()
            if not item:
                continue
            result.add(item if item.startswith(".") else f".{item}")
    return result


def include_path(path: Path, root: Path, extensions: set[str], includes: list[str], excludes: list[str]) -> bool:
    rel = path.relative_to(root).as_posix()
    if path.suffix.lower() not in extensions:
        return False
    if includes and not any(fnmatch.fnmatch(rel, pattern) for pattern in includes):
        return False
    if excludes and any(fnmatch.fnmatch(rel, pattern) for pattern in excludes):
        return False
    return True


def collect_local(target: Path, extensions: set[str], includes: list[str], excludes: list[str]) -> list[dict[str, object]]:
    if target.is_file():
        root = target.parent
        files = [target] if include_path(target, root, extensions, includes, excludes) else []
    else:
        root = target
        files = [
            path
            for path in target.rglob("*")
            if path.is_file() and include_path(path, root, extensions, includes, excludes)
        ]

    items: list[dict[str, object]] = []
    for path in sorted(files):
        try:
            text = path.read_text(encoding="utf-8")
            encoding = "utf-8"
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8", errors="replace")
            encoding = "utf-8-replace"
        rel = path.relative_to(root).as_posix() if target.is_dir() else path.name
        items.append(
            {
                "kind": "file",
                "path": str(path),
                "relative_path": rel,
                "encoding": encoding,
                "lines": text.count("\n") + (1 if text else 0),
                "characters": len(text),
            }
        )
    return items


def fetch_url(url: str, timeout: int) -> tuple[str, str]:
    request = urllib.request.Request(url, headers={"User-Agent": "docs-proofreader-skill/1.0"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        content_type = response.headers.get("Content-Type", "")
        raw = response.read()
    charset = "utf-8"
    for part in content_type.split(";"):
        part = part.strip()
        if part.lower().startswith("charset="):
            charset = part.split("=", 1)[1].strip()
            break
    text = raw.decode(charset, errors="replace")
    if "html" in content_type.lower() or text.lstrip().lower().startswith("<!doctype html") or "<html" in text[:500].lower():
        parser = TextExtractor()
        parser.feed(text)
        text = parser.text()
    return text, content_type


def safe_snapshot_name(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    host = parsed.netloc.replace(":", "_")
    path = parsed.path.strip("/").replace("/", "__") or "index"
    return f"{host}__{path}.txt"


def write_snapshot(output_dir: Path, name: str, text: str) -> str:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / name
    path.write_text(text, encoding="utf-8")
    return str(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("targets", nargs="+", help="Local files/directories or HTTP(S) URLs to collect.")
    parser.add_argument("--ext", action="append", help="Comma-separated extension list for local files.")
    parser.add_argument("--include", action="append", default=[], help="Glob pattern relative to local root.")
    parser.add_argument("--exclude", action="append", default=[], help="Glob pattern relative to local root.")
    parser.add_argument("--output-dir", type=Path, help="Write collected text snapshots to this directory.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of a text summary.")
    parser.add_argument("--timeout", type=int, default=20, help="URL fetch timeout in seconds.")
    args = parser.parse_args()

    extensions = parse_extensions(args.ext)
    items: list[dict[str, object]] = []
    errors: list[dict[str, str]] = []

    for raw_target in args.targets:
        if is_url(raw_target):
            try:
                text, content_type = fetch_url(raw_target, args.timeout)
                item: dict[str, object] = {
                    "kind": "url",
                    "url": raw_target,
                    "content_type": content_type,
                    "lines": text.count("\n") + (1 if text else 0),
                    "characters": len(text),
                }
                if args.output_dir:
                    item["snapshot"] = write_snapshot(args.output_dir, safe_snapshot_name(raw_target), text)
                items.append(item)
            except (urllib.error.URLError, TimeoutError, OSError) as exc:
                errors.append({"target": raw_target, "error": str(exc)})
            continue

        target = Path(raw_target).expanduser()
        if not target.exists():
            errors.append({"target": raw_target, "error": "path does not exist"})
            continue
        local_items = collect_local(target, extensions, args.include, args.exclude)
        if args.output_dir:
            for item in local_items:
                source_path = Path(str(item["path"]))
                text = source_path.read_text(encoding="utf-8", errors="replace")
                item["snapshot"] = write_snapshot(args.output_dir, source_path.name + ".txt", text)
        items.extend(local_items)

    result = {"items": items, "errors": errors}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for item in items:
            label = item.get("relative_path") or item.get("url") or item.get("path")
            print(f"{item['kind']}: {label} ({item['lines']} lines, {item['characters']} chars)")
            if "snapshot" in item:
                print(f"  snapshot: {item['snapshot']}")
        for error in errors:
            print(f"ERROR: {error['target']}: {error['error']}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
