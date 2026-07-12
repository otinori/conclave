# AGENTS.md — Conclave

汎用 AI エージェント向けのリポジトリ作法（Claude Code / Codex 共通）。

## 最初に読む
- `HANDOVER.md` — 申し送り（前回どこまで / 次に何を / 触るな注意）。
- `README.md` — 何の製品か・構成・クイックスタート。

## このリポジトリの性質
- Codex / Claude Code の**プラグイン配布物**。`skills/`・`commands/`・`hooks/`・`templates/` と
  plugin manifest（`.claude-plugin/` / `.codex-plugin/`）はリポジトリ直下固定（プラグイン仕様）。
- ユーザーデータ（workspace 側 `.conclave/`）は配布物と分離。**更新で上書きしない。**

## ドキュメントの置き場所
- 仕様: `docs/design/spec/`（`SPEC-xxxx-*.md`） / 構成: `docs/design/architecture.md`
- 使い方: `docs/manual/`（`usage.md` / `install.md` ほか） / 運用・撤退条件: `docs/ops/`
- 利用者のセッション記録（勤怠・議事録等）は workspace 側 `.conclave/` に生成される。配布物（本リポジトリ）には含まれないユーザーデータであり、`conclave-disclosure` skill が開示窓口となる（`.gitignore` 対象）

## 作業管理
- アクティブ課題: `tasks/TASKS.md` / 積み残し: `tasks/backlog.md` / 完了: `tasks/done/`

## バージョン
- 正本は `VERSION`（現 `0.6.0.1-PoC`）。変更履歴は `CHANGELOG.md`（Keep a Changelog）。
