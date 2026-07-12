---
description: 多角的な議論のために Conclave ペルソナを召喚する
argument-hint: personas: [...], confidentiality: PUBLIC|INTERNAL|CONFIDENTIAL, topic: ..., [--bank <name>]
---

`conclave-summon` スキルを使い、ローカルのペルソナ YAML から Conclave セッションを
開始する。

`skills/conclave-summon/SKILL.md` のワークフローに従うこと:

1. `.conclave/config.yaml` を読む。
2. `--bank <name>` が指定された場合、まずそのバンク（`sync.banks.<name>`）から
   要求されたペルソナをプロジェクトへ取り込む — スキルファイルの
   「Bank-based Summon」を参照。バンクの clone/fast-forward には
   `conclave-bank-sync` を使う。
3. `.conclave/personas/<guild>/<persona-id>/` 配下で各ペルソナを探す。
4. `identity.yaml` と `growth.yaml` を読む。
5. 召喚内容を検証する（人数、ライセンス、必須 L1 フィールド）。
6. ファシリテーターなしで3体以上召喚する場合は候補を提案する。
7. `sess-YYYYMMDD-HHMMSS` 形式の id で
   `.conclave/sessions/<session-id>/meta.yaml` を作成する。
8. 召喚したペルソナとして応答し、各人の口調を明確に書き分ける。

`confidentiality` が未指定で、かつ設定が明示的な宣言を要求している場合は、
開始前にユーザーへ確認すること。

ユーザー入力: $ARGUMENTS
