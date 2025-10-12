# -*- coding: utf-8 -*-
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tools.generate_index import load_metadatas, render  # noqa: E402
import yaml  # noqa: E402


def test_generate_index_orders_by_date_desc(tmp_path):
    casebook = tmp_path / "casebook"
    (casebook / "household" / "202401-someone-a").mkdir(parents=True)
    (casebook / "economy" / "202510-someone-b").mkdir(parents=True)

    # 古い
    (casebook / "household" / "202401-someone-a" / "metadata.yaml").write_text(
        yaml.safe_dump({
            "title": "old",
            "author": "a",
            "date": "20240101",
            "domain": "household",
            "slug": "202401-someone-a",
            "data_sources": [{"name": "n", "provider": "p", "url": "https://example.org", "terms_of_use": "x"}],
            "code_license": "MIT"
        }, allow_unicode=True, sort_keys=False),
        encoding="utf-8"
    )
    # 新しい
    (casebook / "economy" / "202510-someone-b" / "metadata.yaml").write_text(
        yaml.safe_dump({
            "title": "new",
            "author": "b",
            "date": "20251024",
            "domain": "economy",
            "slug": "202510-someone-b",
            "data_sources": [{"name": "n", "provider": "p", "url": "https://example.net", "terms_of_use": "y"}],
            "code_license": "MIT"
        }, allow_unicode=True, sort_keys=False),
        encoding="utf-8"
    )

    items = load_metadatas(casebook)
    assert len(items) == 2
    # 降順（新→古）
    assert items[0]["title"] == "new"
    assert items[1]["title"] == "old"

    md = render(items)
    assert "| economy | 20251024 | new | `202510-someone-b` | b |" in md