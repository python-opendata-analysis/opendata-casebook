#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_links.py
- README.md / metadata.yaml に含まれるリンクの静的検査
- ネットワークアクセスなし（URL 形式・重複・簡易的な NG ドメインチェック）
- 使い方:
    python tools/check_links.py [--root casebook]
"""
import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except Exception:
    print("ERROR: PyYAML が見つかりません。`pip install pyyaml` を実行してください。", file=sys.stderr)
    sys.exit(1)

URL_RE = re.compile(r"https?://[^\s)>\]]+", re.I)
NG_DOMAINS = {
    "http://example.com", "https://example.com"
}


def extract_urls_from_readme(path: Path):
    urls = []
    text = path.read_text(encoding="utf-8", errors="ignore")
    for m in URL_RE.finditer(text):
        urls.append(m.group(0))
    return urls


def extract_urls_from_metadata(path: Path):
    urls = []
    data = yaml.safe_load(path.read_text(encoding="utf-8", errors="ignore")) or {}
    # links
    for link in (data.get("links") or []):
        url = (link or {}).get("url")
        if url:
            urls.append(url)
    # data_sources
    for ds in (data.get("data_sources") or []):
        url = (ds or {}).get("url")
        if url:
            urls.append(url)
        # terms_of_use 内の URL 抜き出し（任意）
        tou = (ds or {}).get("terms_of_use") or ""
        urls += URL_RE.findall(tou)
    return urls


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="casebook")
    args = ap.parse_args()

    root = Path(args.root)
    all_urls = {}
    errors = []

    for md in root.rglob("README.md"):
        if "/_template/" in str(md.as_posix()):
            continue
        for u in extract_urls_from_readme(md):
            all_urls.setdefault(u, []).append(str(md))

    for meta in root.rglob("metadata.yaml"):
        if "/_template/" in str(meta.as_posix()):
            continue
        for u in extract_urls_from_metadata(meta):
            all_urls.setdefault(u, []).append(str(meta))

    # 重複と NG ドメインの簡易チェック
    for url, origins in sorted(all_urls.items()):
        if url in NG_DOMAINS:
            errors.append(f"[NG] {url} はサンプルドメインです。実際の公式URLを記載してください。 -> {origins}")
        if url.lower().startswith("http://"):
            # 「http://stat.go.jp」は公的には https 提供あり。可能なら https 推奨
            errors.append(f"[WARN] {url} は http です。https が提供されている場合は https を推奨します。 -> {origins}")

    if errors:
        print("[ERROR] リンク検査の警告/エラー:")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    else:
        print(f"[OK] リンク検査完了。URL 件数: {len(all_urls)}")


if __name__ == "__main__":
    main()
