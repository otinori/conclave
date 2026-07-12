# ペルソナ作成ガイド

ペルソナは plugin の内部ではなく、ユーザー所有の workspace データ配下に置く:

```text
.conclave/personas/<guild>/<persona-id>/
  identity.yaml
  growth.yaml
```

## identity.yaml の必須項目

すべての `identity.yaml` は以下を含む必要がある:

- `schema_version: "1.0"`
- 一意な `id`
- `Use when` で始まる、または `Use when` を含む `description.en`
- `description.ja`
- `guild`
- `license: internal` または `external_reviewer`
- `kpis` を4件以上
- `role.id` と `role.ja`
- `expertise` を1件以上
- `profile`
- `personality`
- `speech_style`
- `behavior`
- `summon_scenarios`

## growth.yaml の必須項目

すべての `growth.yaml` はペルソナ id と空の memory から始める:

```yaml
schema_version: "1.0"
persona_id: <persona-id>
memory_entries: []
updated_beliefs: []
```

`growth.yaml` への追記は蒸留の承認後にのみ行う。持論が本人の言葉で言い換え可能になった時点で、記憶エントリは承認済みとみなされる。

## L2 類似度チェック

ペルソナを新規作成・fork する前に、同じギルド内の既存ペルソナと比較する:

- KPI重複率 80% 以上: 追加前に見直す。
- KPI重複率 60〜80%: 警告を出し、明示的な承認を求める。
- KPI重複率 60% 未満: MVP としては許容範囲。

fork したペルソナは少なくとも1つのKPIを変更しなければならず、fork元の `growth.yaml` をコピーしてはならない。
