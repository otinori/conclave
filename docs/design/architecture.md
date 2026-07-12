# Architecture — Conclave

> いまどう出来ているか（現在形）。採否の理由は `.udr/` の UDR-ID をリンクで参照する。

Conclave は Codex / Claude Code の **プラグイン配布物**であり、サーバーや MCP 通信を持たない
Skills ベースの MVP。プラグイン仕様上、以下はリポジトリ直下に固定配置される。

## 成果物（配布レイアウト）

| 構成要素 | 役割 |
|---------|------|
| `.claude-plugin/`, `.codex-plugin/` | 各プラットフォームの plugin manifest（分離） |
| `skills/` | Conclave エンジン Skills（Codex / Claude Code 共通、計 14） |
| `commands/` | Claude Code 用 slash commands（計 16） |
| `hooks/` | retro リマインドの native フック（`hooks.json` + 判定スクリプト） |
| `templates/` | workspace 側 `.conclave/` 用テンプレート |
| `samples/.conclave-sample/` | 最小サンプル workspace |

## 配布物とユーザーデータの境界
- 更新してよい配布物: `skills/`, `templates/`, `docs/`, `samples/`
- 保護するユーザーデータ: workspace 側の `.conclave/`（プラグイン更新で上書きしない）

## 仕様の正本
- 全体概要: `docs/design/spec/SPEC-0001-overview.md`
- MVP 仕様: `docs/design/spec/SPEC-0002-mvp.md`
- 将来 MCP 化: `docs/design/spec/SPEC-0003-final.md`
