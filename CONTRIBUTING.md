# 🤝 貢献・提供ガイド - Open Data Casebook

このドキュメントは、**オープンデータの分析・活用事例を投稿・修正・リンク提供する方向け**のガイドです。  
事例の追加や編集を行う際は、以下の手順とルールを必ずご確認ください。

---

## 🧭 ディレクトリ構成ルール

各事例は次の形式で配置します：

```

casebook/{domain}/{slug}/

````

| 要素 | 内容 | 例 |
| ---- | ---- | ---- |
| **domain** | 分析対象分野 | `population`, `household`, `living`, `industry`, `trade`, `economy`, `finance`, `health`, `education`, `environment`, `region`, `common`, `event` |
| **slug** | 一意な識別子（`YYYYMM-author-topic` 推奨） | `202510-yourname-householdanalysis` |

---

## 📂 新しい事例を追加する手順

### 1) テンプレートをコピー
`_template/` をコピーして新しいフォルダを作成します。以下はShellのコマンドの例です。

```bash
cp -r casebook/_template casebook/{domain}/{slug}
````

### 2) ファイルを編集

| ファイル名                  | 内容                                  |
| ---------------------- | ----------------------------------- |
| `README.md`            | 分析の概要・目的・主要な手法・データ取得手順（任意）          |
| `metadata.yaml`        | タイトル、分野、著者、日付、データ出典、ライセンス、リンク、要約、タグ |
| `*.ipynb` または `*.py`   | 再現可能な分析コード                          |
| `requirements.txt`（任意） | 必要なライブラリを記載                         |

> Notebook は保存前に **カーネルをリスタートし、出力を全てクリア** してください。

---

## 🧾 `metadata.yaml` の記入例

```yaml
title: "家計調査と小売物価統計調査"
author: "your_name"
date: "20251024"
domain: "household"
slug: "202510-yourname-householdanalysis"

data_sources:
  - name: "家計調査結果"
    provider: "総務省統計局"
    url: "http://www.stat.go.jp/data/kakei/index.htm"
    terms_of_use: >
      出典明記が必要。編集・加工した場合はその旨も記載。詳細は https://www.stat.go.jp/info/riyou.html
      例）「家計調査結果」（総務省統計局）（当該ページURL）（○年○月○日に利用）

  - name: "消費者物価指数（CPI）"
    provider: "総務省統計局"
    url: "http://www.stat.go.jp/data/cpi/index.htm"
    terms_of_use: >
      出典表記（総務省「消費者物価指数」）が必要。詳細は https://www.stat.go.jp/info/riyou.html

code_license: "MIT"
# notebook_license: "CC BY 4.0"   # 任意
links:
  - label: "note"
    url: "https://note.com/example"
  - label: "GitHub"
    url: "https://github.com/yourname/opendata-example"

description: >
  家計・小売物価・CPI を用いて支出と物価の関係を可視化。

tags:
  - household
  - CPI
  - Python
```

**記載時の注意点**

* `data_sources` は Notebook 内の参照 URL と一致させてください。
* 各データの利用規約（出典明記・加工明記など）を `terms_of_use` に記載してください。
* `links` には公開している記事・リポジトリなどの URL を記入してください。
---

## 🔗 リンクのみを紹介したい場合

Zenn、note、Qiita など外部記事へのリンクだけを紹介したい場合は、Issue を作成してください。

* テンプレート名：**「🔗 Link submission」**
* 記入項目：タイトル、domain（自由入力）、URL、簡単な概要
* CODEOWNERS（運営チーム）が確認のうえ、代行で登録します。

---

## 🧪 PR 前の事前チェック

* [ ] `casebook/{domain}/{slug}/` 構成に沿っている
* [ ] 著作権・ライセンス条件を確認した
* [ ] `metadata.yaml` に出典・利用規約の要点を明記した
* [ ] API Key を Notebook や環境変数ファイルに含んでいない
* [ ] 容量の大きい外部データファイルを含んでいない（API 等で再取得できる形）
* [ ] Notebook を保存前にリスタートし、不要な実行結果を削除した

---

## 🧰 補助スクリプト（tools/）

投稿内容の検証や一覧生成を自動化するためのスクリプトが用意されています。
PR 前の自己確認に利用してください。

```bash
# メタデータの構文検証
python tools/validate_metadata.py

# 外部リンクの死活確認
python tools/check_links.py

# 登録事例の一覧を生成（CASE_INDEX.mdを更新）
python tools/generate_index.py > CASE_INDEX.md
```

---

## ⚖️ データの利用規約と著作権

各事例で使用する統計・オープンデータは、提供元の利用規約に従って利用してください。
投稿者は、利用条件を確認し、`metadata.yaml` に出典と要点を記載する責任を負います。

---

## 📄 コード・記事のライセンス

* **コード**：MIT（または `metadata.yaml` に準拠）
* **Notebook・記事**：CC BY 4.0（任意）
* **データ**：各提供元の利用規約に従う

> ⚠️ データファイルはリポジトリに含めないでください。公的サイトや API から再取得できる形で共有してください。

---

## 🚀 Pull Request の作成

1. ブランチを作成

   ```bash
   git checkout -b add-{domain}-{topic}
   ```
2. 変更をコミット
3. PR を作成し、テンプレート（`.github/PULL_REQUEST_TEMPLATE.md`）に沿って内容を記入

---

## 🕵️‍♀️ レビュー方針

レビューでは **分析内容の正否ではなく構成と公開適正を確認** します。

* `metadata.yaml` の出典・利用規約が正しいか
* 公的統計やオープンデータのライセンス条件に従っているか
* ファイル構成・命名がルールに沿っているか
* 不要な実行結果や容量の大きいデータを含まないか
* CODE_OF_CONDUCT.md に反していないか

> 💡 分析手法や技術的内容は投稿者の責任で公開してください。議論・改善提案は [Discussions](https://github.com/yourname/opendata-casebook/discussions) を利用できます。

