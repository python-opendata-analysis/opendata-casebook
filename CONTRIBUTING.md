# 🤝 貢献・提供ガイド - Open Data Casebook

このドキュメントは、**オープンデータの分析・活用事例の追加・修正・リンク提供などを行う方**のための投稿ガイドです。

事例の投稿やリンク紹介を行う前に、必ず本ドキュメントをご確認ください。

---

## 📘 概要

**Open Data Casebook** は、書籍『[Pythonではじめるオープンデータ分析 ―経済統計の取得からデータハンドリング、可視化、分析まで―](https://www.kspub.co.jp/book/detail/5412251.html)』に関連するオープンデータや公的統計を活用した分析事例を共有するリポジトリです。

---

## 🧭 ディレクトリ構成ルール

各事例は以下の形式で配置します。

```

casebook/{domain}/{source_type}/{slug}/

````

| 要素 | 内容 | 例 |
|------|------|----|
| **domain** | 分析対象分野 | `population`, `household`, `economy`, `industry`, `education`, `environment`, `health`, `region`, `event`, `common` など|
| **source_type** | 事例の形式 | `article`, `project` |
| **slug** | 一意な識別子（半角英数字・ハイフン） | `household_expenditure_zenn-yourname-2025-02` |

> 年単位のディレクトリは設けません。**年や日付は `metadata.yaml` の `date` に記載**してください。

---

## 📂 新しい事例を追加する手順

### 🔹 1. テンプレートをコピーする

新しい分析事例を追加する場合は、 `_template/` をコピーしてフォルダを作成します。

```bash
cp -r casebook/_template casebook/{domain}/{source_type}/{slug}
````

---

### 🔹 2. ファイルを編集する

以下のファイルを必ず編集・作成してください。

| ファイル名                              | 内容                           |
| ---------------------------------- | ---------------------------- |
| `README.md`                        | 分析概要、目的、データ取得方法、実行方法、結果概要を記載 |
| `metadata.yaml`                    | タイトル、分野、日付、著者、ライセンス、出典などを記載  |
| `analysis.ipynb` または `src/main.py` | 分析コード（再現可能な形で記載）             |
| `requirements.txt`（任意）             | 必要な Python パッケージを記載          |

> Notebook をアップロードする際は、**カーネルをリスタートして不要なデータが含まれない状態で保存**してください。

---

### 🔹 3. `metadata.yaml` の記入ルール

例：

```yaml
title: "家計支出の地域比較"
domain: "household"
source_type: "article"
author: "yourname"
date: "2025-02-10"
license: "CC BY 4.0"
data_sources:
  - name: "総務省 家計調査"
    url: "https://www.e-stat.go.jp/"
  - name: "RESAS API"
    url: "https://opendata.resas-portal.go.jp/"
links:
  - label: "Zenn 記事"
    url: "https://zenn.dev/yourname/articles/household-example"
description: "家計支出の地域間比較を行い、年次傾向を可視化した事例。"
```

#### 記載の注意点

* **`license`** はソースコードと記事のライセンスを記載してください（例：MIT, CC BY 4.0 など）。
* **データ利用のライセンス・著作権**は投稿者が必ず確認してください。
* 参考にしたデータの出典（e-Stat, RESAS, IMF など）を `data_sources` に明記してください。

---

## 🔗 リンクのみを紹介する場合

Zenn、note、Qiita などの外部記事を紹介したい場合は、
Issue を作成してください。

* テンプレート：「🔗 Link Submission」
* 記入項目：

  * 記事タイトル
  * 分野（domain）
  * リンクURL
  * 簡単な概要（100文字以内）

> CODEOWNER（運営チーム）が内容を確認し、代わりにリポジトリへ登録します。

---

## 🧪 確認・テスト

PR を送る前に、以下を確認してください。

### ✅ チェックリスト

* [ ] データのライセンスを確認した
* [ ] `metadata.yaml` を記載した
* [ ] Notebook 内の不要な出力を削除した
* [ ] コード実行に必要なライブラリを `requirements.txt` に記載した
* [ ] `README.md` に実行手順・出典・目的を記載した

---

## 🧰 開発補助ツール

投稿内容の整合性を確認するため、`tools/` に補助スクリプトを用意しています。

### メタデータ検証

```bash
python tools/validate_metadata.py
```

### リンクチェック

```bash
python tools/check_links.py
```

### 一覧生成

```bash
python tools/generate_index.py > CASE_INDEX.md
```

---

## ⚖️ データのライセンスと著作権

投稿者は、使用したデータの利用規約・著作権を**自ら確認し明記**してください。

参考：
書籍『[Pythonではじめるオープンデータ分析](https://www.kspub.co.jp/book/detail/5412251.html)』の
「1.2 データの利用規約と著作権について」および
[terms_of_use ディレクトリ](https://github.com/python-opendata-analysis/python-opendata-analysis-book/tree/main/terms_of_use)

---

## 📄 コード・記事のライセンス

* **コード・スクリプト**：MIT または各事例の `metadata.yaml` に準拠
* **記事・Notebook**：CC BY 4.0 を推奨
* **データ**：各 API・公的機関のライセンスに従うこと

> ⚠️ データファイルはリポジトリに含めないでください。
> API やスクリプトによる再現可能な形で共有してください。

---

## 🚀 Pull Request の作成

1. main ブランチから派生したブランチを作成します。
   例：

   ```bash
   git checkout -b add-household-example
   ```
2. 新しい事例を追加してコミットします。
3. Pull Request を作成し、以下を記入します：

   * 目的・背景
   * 使用データと出典
   * 主な結果・可視化概要
   * ライセンス情報

> PR テンプレート（`.github/PULL_REQUEST_TEMPLATE.md`）に沿って記入してください。

---

## 🗣 Discussions・提案

* 分類の追加や構成変更の提案
* 教育・イベントとの連携アイデア
  などは **GitHub Discussions** で議論可能です。

---

## 🙏 謝辞

本プロジェクトは、オープンデータの利活用を広げるため、
書籍読者・研究者・実務者の皆さまのご協力によって成り立っています。
貢献いただいたすべての方に深く感謝します。

---

