---
name: conclave-distill
description: |
  直近の Conclave 勤怠から memory 候補を提示する。ユーザーが @conclave distill
  を求めたとき、memory_seeds を集約したいとき、または growth.yaml を変更せず
  に成長候補を提案してほしいときに使う。
---

# Conclave Distill

勤怠記録を蒸留し、成長メモリの候補案を提示する。

## ワークフロー

1. 対象ペルソナの `identity.yaml` と `growth.yaml` を読む。
2. 直近の `.conclave/attendance/<persona-id>/*.yaml` を読む。
3. `memory_seeds` を集約する。
4. seeds を既存の `memory_entries` と `updated_beliefs` に照らして比較する。
5. 1〜3件の候補を提示する:
   - `fact`
   - `proposed_interpretation`
   - 出典となった勤怠ファイル
   - 該当すれば `superseded_belief` の可能性
6. ユーザーには、`$conclave-distill-accept` を通じて解釈をペルソナ自身の言葉で
   言い直すことによってのみ受け入れるよう求める。

## ルール

- このスキル内では `growth.yaml` を絶対に編集しない。
- ユーザーが承認済みの解釈を提供するまで、繰り返された事実を持論として
  扱わない。
- fact と judgment を分離したままにする。
- 確信度が低い場合、候補の提示数を減らす。
