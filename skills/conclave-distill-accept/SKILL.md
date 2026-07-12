---
name: conclave-distill-accept
description: |
  Conclave の蒸留候補をペルソナの成長メモリに受け入れる。ユーザーが
  @conclave distill-accept を求めたとき、candidate/interpretation を渡した
  とき、または検証済みの memory エントリを growth.yaml に追記したいときに
  使う。
---

# Conclave Distill Accept

受け入れられた蒸留結果をペルソナの `growth.yaml` に追記する。

## 必須入力

- ペルソナ id
- 受け入れられた候補の事実 (fact) または出典
- ユーザーが与えた、ペルソナ自身の言葉による解釈

任意:

- `supersedes`
- トリガー種別・出典・理由

## ワークフロー

1. ペルソナの `identity.yaml` と `growth.yaml` を読む。
2. 解釈が提案された候補の単なるコピーでないことを確認する。
3. 次の memory id を採番する: `M-YYYYMMDD-NN`。
4. 以下を含む `memory_entries` 項目を追記する:
   - `fact.content`
   - `fact.license`
   - `fact.source`
   - `fact.date`
   - `judgment.persona`
   - `judgment.interpretation`
   - `judgment.license`
5. ユーザーが `supersedes` を指定した場合、`superseded_belief` を追加する。
6. 持続的な持論が変わった場合、`updated_beliefs` を追記または更新する。
7. 変更した正確なファイルを報告する。

## ルール

- 既存の memory エントリを保持する。
- 新しい項目は `memory_entries:` リストの**中に**挿入する。ファイル末尾への
  追記ではない。`growth.yaml` には通常 `memory_entries:` の後に
  `updated_beliefs:` ブロックがあり、EOF 追記だと新エントリが
  `updated_beliefs` の下に静かにネストしてしまう。YAML のインデントを
  リストと揃えること。
- fact のライセンスは共有可能な場合があるが、judgment のライセンスは
  ペルソナ固有のまま残す。
- 解釈が欠けている場合、編集せずそれを求める。
