---
description: 既存の Conclave ペルソナを新規ペルソナへ fork する（growth は空で開始）
argument-hint: source: <path>, target_guild: <guild>, target_id: <id>
---

`conclave-fork-persona` スキルを使い、既存の identity から差異を保ちつつ新規
ペルソナを作成する。

`skills/conclave-fork-persona/SKILL.md` のワークフローに従うこと:

1. パスまたはサンプル id で元ペルソナを特定する。
2. 元の `identity.yaml` を読む。
3. 対象の `id` と `guild` を収集する。
4. 少なくとも1つの KPI 変更を必須とする。KPI が完全一致することは禁止する。
5. role・profile・speech_style の変更を推奨する。
6. `/conclave-create-persona` と同じ L1・L2・容量チェックを実施する。
7. `derived_from`（元のパス、forked_at、changes_from_source）を含めて
   対象の `identity.yaml` を書き込む。
8. 新規の空の `growth.yaml` を書き込む。

元の `growth.yaml` を絶対にコピーしない。元ファイルは保持する。対象 id が既に
存在する場合は停止し、新しい id を尋ねる。

ユーザー入力: $ARGUMENTS
