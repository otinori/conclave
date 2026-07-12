---
name: conclave-create-persona
description: |
  対話形式で新規 Conclave ペルソナを作成する。ユーザーが @conclave create-persona /
  add-persona を求めたとき、または新しい
  .conclave/personas/<guild>/<persona-id> の identity.yaml / growth.yaml が
  必要なときに使う。
---

# Conclave Create Persona

ユーザーの `.conclave/` データにペルソナをゼロから作成する。

## ワークフロー

1. `guild` と `id` を収集する。
2. `.conclave/personas/` 全体で id の一意性を確認する。
3. `limits.max_personas` と `limits.max_personas_per_guild` を確認する。
4. 必須の L1 フィールドを収集する:
   - `description.en`（`Use when` を含むこと）
   - `description.ja`
   - `license`
   - 4 件以上の `kpis`
   - `role.id` と `role.ja`
   - 1 件以上の `expertise`
   - `profile`
   - `personality`
   - `speech_style`
   - `behavior`
   - `summon_scenarios`
5. 書き込み前に同ギルドの既存ペルソナと KPI の重複度を提示する。
6. `.conclave/personas/<guild>/<persona-id>/identity.yaml` を書き込む。
7. `.conclave/personas/<guild>/<persona-id>/growth.yaml` を、空の
   `memory_entries` と `updated_beliefs` で書き込む。

## L2 類似度

同ギルドの既存ペルソナに対して簡易な KPI 重複度を計算する:

- 80% 以上: 修正されるか明示的に承認されるまで書き込まない。
- 60〜80%: 警告し、確認を求める。
- 60% 未満: 許容範囲。

## ルール

- 作成後は、ユーザーが明示的に identity を編集しない限り `identity.yaml` を
  安定させたままにする。
- `$conclave-design-persona` 経由で作成されたペルソナでない限り、成長層の
  種を仕込まない。
