---
name: conclave-dismiss
description: |
  Conclave セッションを終了する。ユーザーが @conclave dismiss を求めたとき、
  召喚したペルソナを退出させたいとき、または議論から勤怠 YAML とセッション
  議事録を生成したいときに使う。
---

# Conclave Dismiss

アクティブな Conclave セッションを終了し、記録を書き込む。

## ワークフロー

1. `.conclave/sessions/` からアクティブなセッションを特定する。
2. その `meta.yaml` と現在の会話コンテキストを読む。
3. 召喚された各ペルソナについて、
   `.conclave/attendance/<persona-id>/<YYYY-MM-DD>.yaml` を作成または追記する。
4. ファシリテータが同席していた場合、
   `.conclave/sessions/<session-id>/minutes.md` を作成または更新する。
5. `meta.yaml` に `ended_at` と `status: closed` を記録する。
6. retro トリガーチェックを実行する（下記参照）。
7. 発火した retro を含め、書き込んだファイルをユーザーに要約する。

## retro トリガーチェック

セッション終了後、`conclave-retro`（自動学習）を実行するかどうかを判断する。
`.conclave/config.yaml` を読み、`retro.auto` が false ならこの節をスキップする。

1. 出席した各ペルソナについて、`.conclave/retro/state.yaml`
   （無ければ新規作成）の召喚カウンタをインクリメントする。
2. 以下のいずれかを満たす場合、このセッションを**大規模タスク**と判定する
   （`retro.big_task` の設定に従う）:
   - `meta.yaml` に `big_task: true` がある、
   - セッションで解決したトピック/保留事項が `retro.big_task.min_topics`
     件以上、
   - `confidentiality` が `CONFIDENTIAL`。
3. 以下の場合に該当ペルソナへ `conclave-retro` をトリガーする:
   - このセッションが大規模タスクである場合（トリガー `big_task`）、または
   - 出席した任意のペルソナが `retro.trigger_after_n_summons` に達した場合
     （トリガー `n_summons`）。
4. 解決済みのペルソナとトリガーを添えて `conclave-retro` スキルにハンドオフ
   する。retro は小さな学習を自動適用し、大きな学習は人間承認待ちに回す
   （時間ベースの週次/月次 retro は dismiss ではなくホスト側のスケジューラが
   発火する）。

このスキルから `growth.yaml` を書き込んではいけない — それは規模ゲート付きの
retro の役割である。

## 勤怠の内容

各レポートには以下を含める必要がある:

- 予定していた貢献
- 実際の貢献
- 予期しなかった観察事項
- あれば KPT の差分
- 後で蒸留するための `memory_seeds` 候補

memory seeds はあくまで候補。`growth.yaml` を更新しない。

## 議事録の内容

`templates/minutes.md.template` を型として使う:

- トピック
- ペルソナごとの主要発言
- 合意事項
- 対立点
- 保留事項
- ファシリテータのメタ観察

## ルール

- 生成するファイルでセッションの機密区分を保持する。
- 議論が対立や保留のまま終わった場合、合意があったことにしない。
- 根拠が不十分な場合は、疎なレポートを書き不明点を明記する。
