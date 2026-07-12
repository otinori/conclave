---
description: ユーザースコープ (~/.conclave) のペルソナを現在のプロジェクトへマージする
argument-hint: "[--persona <id>] [--guild <guild>]"
---

`conclave-pull-persona` スキルを使い、個人のペルソナプールからこのプロジェクトへ
ペルソナを取り込む。

`skills/conclave-pull-persona/SKILL.md` のワークフローに従うこと:

1. `.conclave/config.yaml` から `sync.user_scope`（既定: `~/.conclave`）を読む。
2. 引数に応じてユーザースコープから候補ペルソナを走査する:
   - `--persona <id>`: 単一ペルソナ
   - `--guild <guild>`: そのギルドの全ペルソナ
   - 引数なし: ユーザースコープの全ペルソナを表示しユーザーに選ばせる
3. 候補を分類する: **新規追加**（プロジェクトに未存在）と
   **差分マージ**（既に存在）。
4. 分類済みのリストを提示し確認を求める。
5. 新規ペルソナ: L1 検証・L2 類似度判定・容量チェックを実施する。
6. 既存ペルソナ: growth.yaml をエントリ単位でマージする。identity.yaml の
   上書きは明示的な人間承認がある場合のみ行う。
7. サマリレポートを出力する: ペルソナごとの追加/スキップ/要確認件数。

ユーザー入力: $ARGUMENTS
