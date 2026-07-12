# Contributing to Conclave

Conclave は Phase α の個人検証向け MVP です。Issue / PR を歓迎します。

## 開発の前提

- 配布物（`skills/` `commands/` `hooks/` `templates/` `docs/` `samples/`）と
  ユーザーデータ（workspace 側の `.conclave/`）は分離します。PR で
  ユーザーデータを混入させないでください。
- skills / commands は実行コードではなく手順書（`SKILL.md` / command md）です。
  挙動を変える場合は対応するドキュメント（README / USAGE / CHANGELOG）も同期してください。

## 変更前のチェック

- `claude plugin validate .` がパスすること（manifest / skill frontmatter 検証）。
- 触れた YAML / JSON が parse できること。
- フックスクリプトを変更したら `python3 -m py_compile hooks/conclave_retro_check.py`。

## コミット / PR

- 1 PR = 1 トピック。CHANGELOG.md に変更を追記してください。
- 機密情報（認証情報・組織固有名・個人情報）を含めないこと。公開リポジトリです。

## 設計の不変点

`docs/design/spec/SPEC-0001-overview.md` の「三つの柱」と「根本宣言（支援機構である）」は変更不可です。
新機能はこれらを壊さない拡張として提案してください（例: `conclave-retro` は柱3を
「自分=ペルソナの解釈」で保ったまま自動学習を追加した拡張です）。
