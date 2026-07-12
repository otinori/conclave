---
description: Conclave の蒸留候補を承認しペルソナの growth.yaml に反映する
argument-hint: persona: <persona-id>, candidate: <n>, interpretation: <persona's own words>
---

`conclave-distill-accept` スキルを使い、承認済みの蒸留結果をペルソナの
`growth.yaml` に追記する。

`skills/conclave-distill-accept/SKILL.md` のワークフローに従うこと:

1. ペルソナの `identity.yaml` と `growth.yaml` を読む。
2. 解釈が提示された候補の単なる複製でないことを確認する。
3. 次の memory id `M-YYYYMMDD-NN` を採番する。
4. `fact.{content,license,source,date}` と
   `judgment.{persona,interpretation,license}` を持つ `memory_entries` 項目を
   追記する。
5. ユーザーが `supersedes` を指定した場合、`superseded_belief` を追加する。
6. 恒常的な持論が変化した場合、`updated_beliefs` を追記または更新する。
7. 変更した正確なファイルを報告する。

必須入力: ペルソナ id、承認済み候補の fact/source、ペルソナ自身の言葉によるユーザー
提供の解釈。
任意: `supersedes`、トリガー種別、source、理由。

解釈が欠けている場合は編集せず、ユーザーに確認すること。

ユーザー入力: $ARGUMENTS
