---
description: ローカルの Conclave ワークスペース（.conclave/ ディレクトリ構造）を初期化する
argument-hint: [optional notes]
---

`conclave-init` スキルを使い、現在のプロジェクトに Conclave ワークスペースを
初期化する。

`skills/conclave-init/SKILL.md` のワークフローに従うこと:

1. `templates/` を含むプラグインルートを特定する。
2. 既存の `.conclave/` を確認し、ユーザーデータを保持する。
3. `.conclave/personas/`・`attendance/`・`sessions/`・`retro/` 配下に
   不足しているディレクトリを作成する。
4. `.conclave/config.yaml` が存在しない場合のみ、
   `templates/config.yaml.template` から作成する。
5. どのファイルを作成し、どの既存ファイルをそのまま残したかを報告する。

ユーザーが明示的に求めない限り、既存の `.conclave/` ファイルを絶対に上書き
しないこと。

ユーザー入力: $ARGUMENTS
