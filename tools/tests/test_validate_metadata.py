# -*- coding: utf-8 -*-
from pathlib import Path
import sys

# tools を import できるようにパスを追加（リポジトリ直下で pytest 実行を想定）
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tools.validate_metadata import load_schema, validate_one  # noqa: E402


def valid_meta(domain="household", slug="202510-well-living-kakei"):  # 著者部にハイフン含む
    return {
        "title": "テスト事例",
        "author": "well-living",
        "date": "20251024",
        "domain": domain,
        "slug": slug,
        "data_sources": [
            {
                "name": "家計調査結果",
                "provider": "総務省統計局",
                "url": "https://www.stat.go.jp/data/kakei/index.htm",
                "terms_of_use": "出典明記。加工時はその旨も明記。https://www.stat.go.jp/info/riyou.html"
            }
        ],
        "code_license": "MIT",
        "language": "ja",
        "links": [{"label": "note", "url": "https://note.com/example"}],
        "description": "短い説明",
        "tags": ["household", "CPI"]
    }


def test_validate_metadata_success(tmp_casebook):
    casebook = tmp_casebook["casebook"]
    meta = valid_meta()
    ddir = casebook / meta["domain"] / meta["slug"]
    ddir.mkdir(parents=True)
    (ddir / "metadata.yaml").write_text(
        __import__("yaml").safe_dump(meta, allow_unicode=True, sort_keys=False),
        encoding="utf-8"
    )

    schema = load_schema()
    errors = validate_one(ddir / "metadata.yaml", schema)
    assert errors == []


def test_validate_metadata_path_consistency_error(tmp_casebook):
    casebook = tmp_casebook["casebook"]
    meta = valid_meta(domain="household", slug="202510-well-living-kakei")
    # わざと domain を異なる場所（economy）に配置
    ddir = casebook / "economy" / meta["slug"]
    ddir.mkdir(parents=True)
    (ddir / "metadata.yaml").write_text(
        __import__("yaml").safe_dump(meta, allow_unicode=True, sort_keys=False),
        encoding="utf-8"
    )

    schema = load_schema()
    errors = validate_one(ddir / "metadata.yaml", schema)
    # validate_one に「パスと metadata の整合チェック」が実装されている前提
    assert any("domain と metadata.domain が一致しません" in e for e in errors)


def test_validate_slug_allows_hyphen_in_author(tmp_casebook):
    casebook = tmp_casebook["casebook"]
    meta = valid_meta(slug="202510-well-living-kakei")  # 著者部に '-' を含む
    ddir = casebook / meta["domain"] / meta["slug"]
    ddir.mkdir(parents=True)
    (ddir / "metadata.yaml").write_text(
        __import__("yaml").safe_dump(meta, allow_unicode=True, sort_keys=False),
        encoding="utf-8"
    )

    schema = load_schema()
    errors = validate_one(ddir / "metadata.yaml", schema)
    assert errors == []
