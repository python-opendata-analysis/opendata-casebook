# Open Data Casebook - オープンデータ分析 事例集サイト

本リポジトリは、書籍『[Pythonではじめるオープンデータ分析 ―経済統計の取得からデータハンドリング、可視化、分析まで―](https://www.kspub.co.jp/book/detail/5412251.html)』の事例集サイトです。  
オープンデータや公的統計を活用した分析・可視化の事例とサンプルコードを公開しています。  
多くは書籍に掲載していない追加事例で、データ分析の共有・学び合い・再利用を促進するためのオープンリポジトリです。  

読者・利用者からの **Pull Request（事例提供）** や **note / Zenn など外部記事のリンク紹介** も受け付けています。

📘 書籍サポートサイト：  
👉 [python-opendata-analysis-book](https://github.com/python-opendata-analysis/python-opendata-analysis-book)

---

## 🧭 本リポジトリについて

**Open Data Casebook** は、人口・家計・生活・金融・経済・産業・教育・地域など、
社会分野ごとのオープンデータ活用事例を整理・共有するリポジトリです。

事例のサンプルコードは **[`casebook/`](./casebook)** に整理されています。 
なお、ワークショップ・講演・イベントで共有された分析コードも`event/` ディレクトリで公開できます。

各事例は、以下の命名・構成を基本とします。

```text
casebook/{domain}/{slug}/
````

| 要素         | 内容                 | 例                                                                                                                   |
| ---------- | ------------------ | ------------------------------------------------------------------------------------------------------------------- |
| **domain** | 分析分野または事例区分        | `population`, `household`, `economy`, `industry`, `education`, `environment`, `health`, `region`, `common`, `event` |
| **slug**   | 一意な識別子（`日付-名前-内容`） | `yyyymm-yourname-content`                                                                                 |

各事例ディレクトリには、以下のファイルを含めてください。

* `README.md`：分析概要、データ取得手順、出典情報
* `metadata.yaml`：分野、日付、データ出典、ライセンスなど
* `.ipynb`（Notebook）または Python スクリプト
* `requirements.txt`（必要に応じて）

**例：**

```text
casebook/
├─ household/
│  └─ 202510-yourname-kakei/
│     ├─ README.md
│     ├─ metadata.yaml
│     └─ 家計調査の分析.ipynb
├─ event/
│  └─ 202602-xxuniv-workshop/
│     ├─ README.md
│     ├─ metadata.yaml
│     └─ 講演資料.ipynb
└─ _template/
   ├─ README.md
   └─ metadata.yaml
```

> Notebook は不要なデータを含めないよう、保存前に **カーネルをリスタート** してください。

---

## 🗂️ リポジトリ構成

```text
.
├─ casebook/                # 各事例
│  ├─ population/           # 人口
│  ├─ household/            # 家計・消費
│  ├─ living/               # 生活
│  ├─ industry/             # 産業・法人・企業
│  ├─ trade/                # 貿易
│  ├─ economy/              # 経済
│  ├─ finance/              # 金融・市場
│  ├─ health/               # 医療・福祉
│  ├─ education/            # 教育
│  ├─ environment/          # 環境
│  ├─ region/               # 地域
│  ├─ common/               # 複数分野にまたがる事例
│  ├─ event/                # 講演・ワークショップ・ハッカソンなどの事例
│  └─ _template/            # 新規事例用テンプレート
│
├─ tools/                   # 検証・補助スクリプト
│  ├─ validate_metadata.py  # metadata.yaml の検証
│  ├─ check_links.py        # 外部リンクの有効性確認
│  ├─ generate_index.py     # 一覧自動生成
│  ├─ schema/               # スキーマ定義
│  └─ templates/            # README・metadata テンプレート
│
├─ .github/                 # GitHub 用設定
│  ├─ ISSUE_TEMPLATE/       # Issue テンプレート
│  ├─ PULL_REQUEST_TEMPLATE.md
│  ├─ CODE_OF_CONDUCT.md
│  └─ CONTRIBUTING.md
│
├─ CASE_INDEX.md            # 自動生成される全事例一覧
└─ README.md                # このファイル
```

---

## 📝 事例の追加方法

### 🔹 新しい事例を追加する場合

1. `_template/` をコピーして新しいフォルダを作成

   ```bash
   cp -r casebook/_template casebook/{domain}/{slug}
   ```
2. `README.md` と `metadata.yaml` を編集
3. 動作確認後、Pull Request を作成

詳細は [`CONTRIBUTING.md`](.github/CONTRIBUTING.md) をご覧ください。

---

### 🔹 リンクのみを紹介する場合

note / Zenn / Qiita などの外部記事を紹介したい場合は、Issue を作成してください。
運営側が内容を確認のうえ登録します。

---

## 💬 コミュニティと連絡

リポジトリに関する質問や提案は、以下の方法で受け付けています。

* 🐛 **Issue**：事例の修正・改善・リンク追加の提案
* 💬 **Discussions**：分析テーマの相談、構成・方針の議論、使い方の質問

> → [Discussions タブ](https://github.com/python-opendata-analysis/opendata-casebook/discussions)

---

## 🧰 補助ツール

```bash
# メタデータ検証
python tools/validate_metadata.py

# リンクチェック
python tools/check_links.py

# 一覧生成
python tools/generate_index.py > CASE_INDEX.md
```

---

## ⚖️ 行動規範

このリポジトリは、オープンデータの分析事例を共有し、知見を広げるための共同の場です。
すべての利用者が安心して参加できるよう、互いを尊重し、丁寧なコミュニケーションを心がけてください。

> → [CODE_OF_CONDUCT.md](.github/CODE_OF_CONDUCT.md)

---

## 📄 データの利用規約と著作権

各事例で使用する統計・オープンデータは、提供元の利用規約に従って利用してください。
統計局・各機関のデータ利用規約は、
[こちらのリンク集](https://github.com/python-opendata-analysis/python-opendata-analysis-book/tree/main/terms_of_use)
に整理しています。

> 各事例の投稿者は、利用データの著作権・利用条件を確認し、
> 必ず `metadata.yaml` に出典・利用規約情報を記載してください。

---

## 📄 ライセンス

* **コード・スクリプト**：MIT License（または各事例の `metadata.yaml` に準拠）
* **Notebook・記事内容**：CC BY 4.0 推奨
* **データ**：各提供元の利用規約に従い、記載してください

> ⚠️ このリポジトリにはデータファイルを含めません。
> 公的機関のサイトや API から再取得できる形式で共有してください。

---

## 🤝 貢献・提供方法

* 事例やサンプルコードの追加・修正 → Pull Request
* 外部記事リンクの紹介 → Issue
* 改善提案・方針相談 → Discussions

貢献の際は [CONTRIBUTING.md](.github/CONTRIBUTING.md) をお読みください。

---

## 📬 お問い合わせ

質問・提案・修正依頼は [Issues](https://github.com/python-opendata-analysis/opendata-casebook/issues)
または [Discussions](https://github.com/python-opendata-analysis/opendata-casebook/discussions) にて受け付けています。

## 📚 関連書籍と関連サイト

📘 書籍：
『[Pythonではじめるオープンデータ分析 ―経済統計の取得からデータハンドリング、可視化、分析まで―](https://www.kspub.co.jp/book/detail/5412251.html)』
💻 サポートサイト：
[python-opendata-analysis-book](https://github.com/python-opendata-analysis/python-opendata-analysis-book)

