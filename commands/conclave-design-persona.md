---
description: 複数ペルソナによる設計会議を通じて新規 Conclave ペルソナを設計する
argument-hint: target_guild: <guild>, intent: <design intent>
---

`conclave-design-persona` スキルを使い、Conclave 自身を使ってペルソナを設計する。

`skills/conclave-design-persona/SKILL.md` のワークフローに従うこと:

1. `target_guild`、希望する役割、設計意図を収集する。
2. 設計パネルを推薦する（ファシリテーション役のペルソナ、同ギルドの参照ペルソナ、
   ライセンスが関わる場合はガバナンス役ペルソナ、採用が関わる場合は現場ペルソナ）。
3. 機密区分を確認する。
4. 明確な合意・対立・保留点を含む設計会議を実施する。
5. `identity.yaml` の草案を作る。
6. 設計セッションの内容と新規ペルソナの根本となる解釈を記述した初期
   memory エントリ1件を含む `growth.yaml` の草案を作る。
7. `.conclave/sessions/<session-id>/minutes.md` にセッション議事録を書く。
8. ユーザー承認後にのみ新規ペルソナを書き込む。

design-persona は初期 growth memory を仕込んでよい（設計会議自体が由来の一部の
ため）。ただし初期判断は必ず新規ペルソナ自身の言葉で記述すること。書き込み前に
L1・L2・容量チェックは通常どおり実施する。

ユーザー入力: $ARGUMENTS
