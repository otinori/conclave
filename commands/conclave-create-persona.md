---
description: 対話形式で新規 Conclave ペルソナを作成する
argument-hint: guild: <guild>, id: <persona-id>, [intent]
---

`conclave-create-persona` スキルを使い、ユーザーの `.conclave/` データにペルソナを
ゼロから作成する。

`skills/conclave-create-persona/SKILL.md` のワークフローに従うこと:

1. `guild` と `id` を収集する。
2. `.conclave/personas/` 全体で id の一意性を確認する。
3. `limits.max_personas` と `limits.max_personas_per_guild` を確認する。
4. 必須の L1 フィールドを収集する（"Use when" を含む description.en、
   description.ja、license、4件以上の kpis、role.id/ja、1件以上の expertise、
   profile、personality、speech_style、behavior、summon_scenarios）。
5. 書き込み前に同ギルドのペルソナと KPI の重複度を表示する。
6. `.conclave/personas/<guild>/<persona-id>/identity.yaml` を書き込む。
7. `memory_entries` と `updated_beliefs` を空にした
   `.conclave/personas/<guild>/<persona-id>/growth.yaml` を書き込む。

L2 類似度判定: KPI 重複度 80% 以上はブロック、60〜80% は警告、60% 未満は許容。

`/conclave-design-persona` を使う場合を除き、growth memory の初期値を仕込まない。

ユーザー入力: $ARGUMENTS
