---
description: レトロスペクティブを実行し growth.yaml へ自動学習する（小さな変化は自動、大きな変化は承認待ち）
argument-hint: "[personas: <ids>] [scope: since:<date>|last_n_sessions:<n>] [dry_run: true]"
---

`conclave-retro` スキルを使い、レトロスペクティブを実行しペルソナの memory を
自動学習する。

`skills/conclave-retro/SKILL.md` のワークフローに従うこと:

1. `.conclave/config.yaml` を読む。`retro.auto` が false かつ手動呼び出しでない
   場合、停止し自動 retro が無効である旨を報告する。
2. 対象ペルソナと範囲を解決する（既定: `last_retro_at` 以降に新しい勤怠がある
   全員）。
3. 各ペルソナについて、`identity.yaml`・`growth.yaml`・範囲内の勤怠と議事録を
   読み、ペルソナ自身の声で KPT レトロスペクティブを構築し、候補となる学びを
   導出する。
4. 変化度ゲートを適用する:
   - SMALL（既存の持論と矛盾しない新しい学び、既定ライセンスの範囲内）→
     ペルソナが自身の解釈を書き、その場で `growth.yaml` に追記する。
   - BIG（持論の反転/上書き、ライセンスの格上げ、CONFIDENTIAL 由来、
     ペルソナ間の持論移転、既存エントリとの矛盾のいずれか）→
     `.conclave/retro/<retro-id>/pending.yaml` に退避し、`growth.yaml` には
     触れない。判断に迷う場合は BIG として扱う。
5. `.conclave/retro/<retro-id>/retro.md` にレトロ記録を書き、
   `.conclave/retro/state.yaml` の `last_retro_at` を更新し召喚カウンタを
   リセットする。
6. ペルソナごとに報告する: 何を自動学習したか、何が人間の承認待ちか、変更した
   正確なファイル。

候補テキストをそのまま `interpretation` にコピーしてはならない — ペルソナは
必ず自身の言葉で言い直すこと（柱3）。保留中の BIG 項目は後で
`/conclave-distill-accept` で解決する。

ユーザー入力: $ARGUMENTS
