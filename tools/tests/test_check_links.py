# -*- coding: utf-8 -*-
from pathlib import Path
import sys
import subprocess

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


def test_check_links_warns_on_http_and_ng_domain(tmp_path):
    # casebook 構造
    ddir = tmp_path / "casebook" / "household" / "202510-someone-topic"
    ddir.mkdir(parents=True)
    # README に http://example.com（NG ドメイン）を入れる
    (ddir / "README.md").write_text(
        "# Sample\n\nSee http://example.com and http://stat.go.jp/data/kakei/index.htm\n",
        encoding="utf-8"
    )
    # metadata にも http URL を入れる
    (ddir / "metadata.yaml").write_text(
        """\
title: "t"
author: "a"
date: "20251024"
domain: "household"
slug: "202510-someone-topic"
data_sources:
  - name: "n"
    provider: "p"
    url: "http://stat.go.jp/data/kakei/index.htm"
    terms_of_use: "see http://stat.go.jp/info/riyou.html"
code_license: "MIT"
language: "ja"
""",
        encoding="utf-8"
    )

    # スクリプト実行（NG/警告があると exit 1 を期待）
    res = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "check_links.py"), "--root", str(tmp_path / "casebook")],
        capture_output=True, text=True
    )
    assert res.returncode != 0
    # 代表的な警告が出ていること
    assert "example.com はサンプルドメイン" in res.stdout or res.stderr
    assert "http です。https が提供されている場合は https を推奨" in (res.stdout + res.stderr)
