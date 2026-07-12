# Handover Memo

作成日: 2026-04-27
更新日: 2026-07-12 (v0.6.0.1-PoC: ドキュメント日本語統一 / 新規リリースとして再起点化)

## 現状

Conclave MVP は v0.6.0.1-PoC として配布パッケージ一式が揃っている。

- plugin manifest (`.codex-plugin/` / `.claude-plugin/`) と self-distributing
  marketplace (`.claude-plugin/marketplace.json`)
- engine skills 14 個 (`skills/`) と slash commands 16 個 (`commands/`)
- retro リマインドの native フック (`hooks/hooks.json` + `conclave_retro_check.py`)
- `.conclave/` 用テンプレート (`templates/`) と最小サンプル (`samples/.conclave-sample/`)
- ドキュメント (`docs/design/` · `docs/manual/` · `docs/ops/`)・`README.md`・`CHANGELOG.md`

変更履歴の詳細は `CHANGELOG.md`、retro 自動学習の仕様は
`docs/manual/retro-auto-learning.md` を参照。

## やり残し（未検証）

1. Codex plugin としての読み込み確認
   - JSON パースは確認済み。Codex UI/ランタイムに local plugin として入れて
     skill が期待通り発火するところは未確認。

2. Skill validator の正式実行
   - PyYAML 導入済み。`conclave-retro` を含む 14 skill の frontmatter 一括検証
     (`quick_validate.py` 相当) はまだ。

3. フックの実ランタイム発火確認
   - 判定スクリプトと settings.json マージ/解除は scratch で E2E 検証済み。
     実 Claude Code セッションで SessionStart フックとして additionalContext が
     注入されるところまでは未確認。

4. `.conclave/` 初期化の実地テスト
   - `/conclave-init` の手順は SKILL.md に記載済みだが、別 workspace での
     end-to-end 生成テストは未実施。

## 課題（標準的な制約）

- `skills/` は手順書としての MVP 実装であり、CLI や MCP のような自動実行コードではない。
  日報・議事録・`growth.yaml` 更新は、エージェントが skill 手順に従って編集する前提。
- YAML の厳密な schema validation はまだない。
- 配布サンプル persona は `sample-facilitator` 1 名のみ。拡充するかは要判断。

## 推奨する次アクション

1. skill validator を正式実行して 14 skill の frontmatter を一括検証する。
2. 一時 workspace で `/conclave-init` → `/conclave-summon` → `/conclave-dismiss` を一度通す。
3. 実セッションで SessionStart フックの発火（retro リマインド注入）を確認する。
