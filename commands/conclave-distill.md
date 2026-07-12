---
description: 直近の Conclave 勤怠から memory 候補を提示する（growth.yaml への書き込みなし）
argument-hint: persona: <persona-id>
---

`conclave-distill` スキルを使い、勤怠記録から memory 候補案を蒸留する。

`skills/conclave-distill/SKILL.md` のワークフローに従うこと:

1. 対象ペルソナの `identity.yaml` と `growth.yaml` を読む。
2. 直近の `.conclave/attendance/<persona-id>/*.yaml` を読む。
3. `memory_seeds` を集約する。
4. 集約した候補を既存の `memory_entries` と `updated_beliefs` と比較する。
5. `fact`、`proposed_interpretation`、出典となる勤怠ファイル、該当すれば
   `superseded_belief` を添えて1〜3件の候補を提示する。
6. `/conclave-distill-accept` を通じ、ペルソナ自身の言葉で解釈を書き直しても
   らうことでのみ承認を受け付けるようユーザーに求める。

このコマンドでは `growth.yaml` を絶対に編集しない。事実層と判断層を分離して
扱うこと。

ユーザー入力: $ARGUMENTS
