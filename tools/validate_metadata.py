#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_metadata.py
- metadata.yaml の検証スクリプト
- 使い方:
    python tools/validate_metadata.py [--root casebook]
"""
import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml  # PyYAML
except Exception:
    print("ERROR: PyYAML が見つかりません。`pip install pyyaml` を実行してください。", file=sys.stderr)
    sys.exit(1)

try:
    import jsonschema
except Exception:
    print("ERROR: jsonschema が見つかりません。`pip install jsonschema` を実行してください。", file=sys.stderr)
    sys.exit(1)

SCHEMA_PATH = Path(__file__).parent / "schema" / "metadata.schema.json"

DATE_RE = re.compile(r"^\d{8}$")              # YYYYMMDD
SLUG_RE = re.compile(r"^\d{6}-[a-z0-9_]+-[a-z0-9_-]+$")  # YYYYMM-author-topic（author は小文字英数/アンダースコア）
URL_RE = re.compile(r"^https?://", re.I)


def load_schema():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def iter_metadata_files(root: Path):
    for p in root.rglob("metadata.yaml"):
        # _template 内はスキップ（必要なら --include-template を追加して運用）
        if "/_template/" in str(p.as_posix()):
            continue
        yield p


def validate_one(path: Path, schema) -> list[str]:
    errors = []
    with open(path, "r", encoding="utf-8") as f:
        try:
            meta = yaml.safe_load(f) or {}
        except Exception as e:
            return [f"[YAML] {path}: 解析エラー: {e}"]

    # JSON Schema 基本検証
    try:
        jsonschema.validate(instance=meta, schema=schema)
    except jsonschema.ValidationError as e:
        errors.append(f"[Schema] {path}: {e.message}")

    # 追加ルール
    # date: YYYYMMDD
    date = meta.get("date")
    if date and not DATE_RE.match(str(date)):
        errors.append(f"[Rule] {path}: date は YYYYMMDD 形式で記載してください（例: 20251024）。")

    # slug: YYYYMM-author-topic
    slug = meta.get("slug", "")
    if slug and not SLUG_RE.match(slug):
        errors.append(f"[Rule] {path}: slug は 'YYYYMM-author-topic' 形式の小文字推奨です（例: 202510-well_living_ry-kakei-kouri）。")

    # domain: 空でないか（形式は自由入力、空チェックのみ）
    if not meta.get("domain"):
        errors.append(f"[Rule] {path}: domain を指定してください。")

    # data_sources: 必須キーと URL・規約要点
    ds = meta.get("data_sources", [])
    if not ds:
        errors.append(f"[Rule] {path}: data_sources を 1 件以上記載してください。")
    else:
        for i, d in enumerate(ds):
            for key in ("name", "provider", "url", "terms_of_use"):
                if not d.get(key):
                    errors.append(f"[Rule] {path}: data_sources[{i}].{key} が不足しています。")
            url = d.get("url", "")
            if url and not URL_RE.match(url):
                errors.append(f"[Rule] {path}: data_sources[{i}].url は http(s) で始まる URL を記載してください。")

    # links: 任意だが、ある場合は URL をチェック
    for i, link in enumerate(meta.get("links", []) or []):
        if not link.get("label"):
            errors.append(f"[Rule] {path}: links[{i}].label が不足しています。")
        if not link.get("url") or not URL_RE.match(link["url"]):
            errors.append(f"[Rule] {path}: links[{i}].url が不正です（http(s) で始まる URL を指定）。")

    # code_license: 必須
    if not meta.get("code_license"):
        errors.append(f"[Rule] {path}: code_license を指定してください（例: MIT）。")

    # パスと metadata の整合性チェック
    # path 例: .../casebook/household/202510-someone-topic/metadata.yaml
    parts = path.parts
    if len(parts) >= 3:
        path_slug = parts[-2]      # metadata.yaml の親ディレクトリ名
        path_domain = parts[-3]    # slug の親ディレクトリ名
        
        meta_domain = meta.get("domain", "")
        meta_slug = meta.get("slug", "")
        
        if meta_domain and path_domain != meta_domain:
            errors.append(f"[Rule] {path}: パスの domain と metadata.domain が一致しません（パス: {path_domain}, metadata: {meta_domain}）。")
        
        if meta_slug and path_slug != meta_slug:
            errors.append(f"[Rule] {path}: パスの slug と metadata.slug が一致しません（パス: {path_slug}, metadata: {meta_slug}）。")

    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="casebook", help="探索ルート（既定: casebook）")
    args = ap.parse_args()

    root = Path(args.root)
    schema = load_schema()

    all_errors = []
    count = 0
    for meta_path in iter_metadata_files(root):
        count += 1
        errs = validate_one(meta_path, schema)
        if errs:
            all_errors.extend(errs)

    if all_errors:
        print("[ERROR] metadata.yaml 検証エラー:")
        for e in all_errors:
            print(" -", e)
        print(f"\n検査対象ファイル: {count} 件 / 失敗: {len(all_errors)} 件")
        sys.exit(1)
    else:
        print(f"[OK] metadata.yaml 検証成功（対象 {count} 件）")


if __name__ == "__main__":
    main()