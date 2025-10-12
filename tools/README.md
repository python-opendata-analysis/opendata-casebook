# 🧰 tools ディレクトリ

`casebook/` の運用を補助するスクリプト群です。

## ファイル構成

```text
tools/
├─ validate_metadata.py      # metadata.yaml の構文・必須項目・書式チェック（JSON Schema + 独自規約）
├─ check_links.py            # README/metadata に含まれる URL の静的検査（形式・重複・NGドメイン）
├─ generate_index.py         # 全事例の索引 CASE_INDEX.md を生成
├─ schema/
│  └─ metadata.schema.json   # metadata.yaml 用 JSON Schema（validate_metadata が参照）
└─ templates/
   └─ metadata.yaml          # 事例メタデータのテンプレート（人間がコピペして使う雛形）
```

> `schema` はプログラム（検証）が読む「仕様」、`templates` は投稿者が読む「雛形」です。

---

## 使い方

### 1) メタデータ検証

```bash
python tools/validate_metadata.py --root casebook
```

* `casebook/**/metadata.yaml` を走査し、スキーマ検証＋独自ルール（`date` 形式、`slug` 形式、`data_sources` 必須キー、パスと値の整合など）を行います。
* エラーがあると **exit code 1** で終了します（CI で使用可能）。

### 2) リンク検査（オフライン静的検査）

```bash
python tools/check_links.py --root casebook
```

* URL 文字列の **形式・重複・一部 NG ドメイン** をチェックします（ネットワークアクセスはしません）。
* 問題があれば **exit code 1**。

### 3) 索引生成

```bash
python tools/generate_index.py > CASE_INDEX.md
```

* 全 `metadata.yaml` を集約し、`CASE_INDEX.md`（domain / date / title / slug / author / links）を出力します。
* 新しい日付順で並び替え。

---

## テストの実行

必要パッケージ（ローカル）:

```bash
pip install pytest pyyaml jsonschema
```

テスト実行:

```bash
pytest -q tools/tests
```

* すべてのテストは **一時ディレクトリ** で仮想的に事例を生成して検査します。
* 既存のリポジトリ内容は変更しません。

---

# GitHub Actions セットアップ

このプロジェクトでは、GitHub Actionsを使用して自動テスト・検証・インデックス生成を行います。

## フォルダ構成

```
.github/
  workflows/
    ci.yml              # テスト・検証ワークフロー
    generate-index.yml  # インデックス生成ワークフロー（手動実行）
```

## ワークフロー概要

### 1. CI（ci.yml）

**トリガー**: `main`、`develop` ブランチへの push / pull request

**実行内容**:
- pytest によるテスト実行
- metadata.yaml の検証（`validate_metadata.py`）
- リンクのチェック（`check_links.py`）

**ジョブ**:
- `test`: pytest を実行してテストスイートをチェック
- `validate`: metadata とリンクの検証を実行

---

### 2. Generate Index（generate-index.yml）

**トリガー**: 手動実行のみ（`workflow_dispatch`）

**実行内容**:
- `CASE_INDEX.md` を生成してアーティファクトとして保存
- ダウンロードしてローカルで確認後、手動でコミット

**動作**:
1. `generate_index.py` を実行して `CASE_INDEX.md` を生成
2. アーティファクトとして保存（7日間保持）
3. ユーザーがダウンロードして内容を確認
4. 問題なければ手動でコミット・プッシュ

**使い方**:
1. GitHub リポジトリの **Actions** タブに移動
2. 左側のワークフロー一覧から **Generate Index (Manual)** を選択
3. **Run workflow** ボタンをクリック
4. ブランチを選択して **Run workflow** を実行
5. ワークフロー完了後、**Artifacts** セクションから `case-index` をダウンロード
6. ダウンロードした `CASE_INDEX.md` を確認
7. 問題なければリポジトリのルートに配置してコミット

---

## セットアップ手順

### 1. ワークフローファイルの配置

リポジトリのルートに以下のファイルを配置してください：

```
.github/workflows/ci.yml
.github/workflows/generate-index.yml
```

### 2. GitHub リポジトリの設定

**手動実行方式では特別な権限設定は不要です。**

CIワークフローは自動的に実行されます。インデックス生成は手動で実行してください。

---

## ローカルでのテスト

GitHub Actionsにプッシュする前に、ローカルで動作確認できます：

```bash
# pytestの実行
pytest -v tools/tests

# metadata検証
python tools/validate_metadata.py --root casebook

# リンクチェック
python tools/check_links.py --root casebook

# インデックス生成
python tools/generate_index.py > CASE_INDEX.md
```

---

## トラブルシューティング

### ワークフローが失敗する場合

1. **Actions タブ**で失敗したワークフローをクリック
2. 失敗したジョブを選択してログを確認
3. エラーメッセージに従って修正

### アーティファクトがダウンロードできない場合

- ワークフローが正常に完了しているか確認
- アーティファクトの保持期間（7日間）を過ぎていないか確認
- 必要に応じてワークフローを再実行

### 依存関係のエラー

ワークフローファイルの `Install dependencies` セクションで必要なパッケージがすべてインストールされているか確認してください。

---

## バッジの追加（オプション）

README.md にステータスバッジを追加できます：

```markdown
![CI](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/CI/badge.svg)
```

`YOUR_USERNAME` と `YOUR_REPO` を実際の値に置き換えてください。

---
