# -*- coding: utf-8 -*-
import textwrap
from pathlib import Path
import pytest
import yaml


@pytest.fixture
def tmp_casebook(tmp_path: Path):
    """
    一時の casebook 構造を作るためのユーティリティ。
    戻り値: dict(domain_dir=Path, case_dir=Path, casebook=Path)
    """
    casebook = tmp_path / "casebook"
    casebook.mkdir()
    return {"casebook": casebook}


def write_yaml(path: Path, data: dict):
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")


def make_case(casebook: Path, domain: str, slug: str, meta: dict, readme: str = "# README\n"):
    ddir = casebook / domain / slug
    ddir.mkdir(parents=True)
    (ddir / "metadata.yaml").write_text(
        yaml.safe_dump(meta, allow_unicode=True, sort_keys=False),
        encoding="utf-8"
    )
    (ddir / "README.md").write_text(readme, encoding="utf-8")
    return ddir
