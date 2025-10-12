#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_index.py
- casebook 以下の metadata.yaml を集約し、CASE_INDEX.md を標準出力に生成
- 使い方:
    python tools/generate_index.py > CASE_INDEX.md
"""
from pathlib import Path
import sys

try:
    import yaml
except Exception:
    print("ERROR: PyYAML が見つかりません。`pip install pyyaml` を実行してください。", file=sys.stderr)
    sys.exit(1)


def load_metadatas(root: Path):
    items = []
    for p in root.rglob("metadata.yaml"):
        if "/_template/" in str(p.as_posix()):
            continue
        try:
            meta = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        except Exception:
            continue
        # 必要フィールドを抽出（存在しない場合は空文字）
        items.append({
            "domain": meta.get("domain", ""),
            "date": meta.get("date", ""),
            "title": meta.get("title", ""),
            "slug": meta.get("slug", ""),
            "author": meta.get("author", ""),
            "links": meta.get("links", []),
            "path": str(p.parent)
        })
    # 新しい日付順（降順）
    items.sort(key=lambda x: x.get("date", ""), reverse=True)
    return items


def render(items):
    lines = []
    lines.append("# CASE INDEX")
    lines.append("")
    lines.append("| domain | date | title | slug | author | links |")
    lines.append("|--------|------|-------|------|--------|-------|")

    for it in items:
        links_cell = ", ".join([f"[{l.get('label','link')}]({l.get('url','#')})" for l in it["links"]]) if it["links"] else ""
        lines.append(f"| {it['domain']} | {it['date']} | {it['title']} | `{it['slug']}` | {it['author']} | {links_cell} |")

    lines.append("")
    lines.append("> 自動生成: `python tools/generate_index.py > CASE_INDEX.md`")
    return "\n".join(lines)


def main():
    root = Path("casebook")
    items = load_metadatas(root)
    print(render(items))


if __name__ == "__main__":
    main()
