---
description: 進行中の Conclave セッションを終了し、勤怠と議事録を書き込む
argument-hint: [optional session-id]
---

`conclave-dismiss` スキルを使い、進行中の Conclave セッションを終了し記録を書き込む。

`skills/conclave-dismiss/SKILL.md` のワークフローに従うこと:

1. `.conclave/sessions/` 内の進行中セッションを特定する。
2. `meta.yaml` と現在の会話コンテキストを読む。
3. 召喚済みの各ペルソナについて `.conclave/attendance/<persona-id>/<YYYY-MM-DD>.yaml`
   を新規作成または追記する。
4. ファシリテーターが同席していた場合、`.conclave/sessions/<session-id>/minutes.md`
   を新規作成または更新する。
5. `meta.yaml` に `ended_at` と `status: closed` を記録する。
6. 書き込んだファイルをユーザーに要約する。

`memory_seeds` は候補提示のみ — ここで `growth.yaml` を更新してはならない。

ユーザー入力: $ARGUMENTS
