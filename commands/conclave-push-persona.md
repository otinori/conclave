---
description: 現在のプロジェクトのペルソナをユーザースコープ (~/.conclave) または名前付き git バンクへ同期する
argument-hint: "[--persona <id>] [--guild <guild>] [--bank <name>]"
---

`conclave-push-persona` スキルを使い、このプロジェクトで育てたペルソナを個人の
ペルソナプールへ、または `--bank <name>` を通じて共有 git バンク
（`sync.banks.<name>`、例 `conclave_persona-bank`）へエクスポートする。

`skills/conclave-push-persona/SKILL.md` のワークフローに従うこと:

1. `.conclave/config.yaml` から `sync.user_scope`（既定: `~/.conclave`）を読む。
2. 引数から対象ペルソナを解決する:
   - `--persona <id>`: 単一ペルソナ
   - `--guild <guild>`: そのギルドの全ペルソナ
   - 引数なし: プロジェクトの全ペルソナを表示しユーザーに選ばせる
3. `--bank <name>` が指定された場合、`sync.banks.<name>` を解決し、まず
   `conclave-bank-sync --bank <name> --mode pull` を実行してバンクの clone を
   最新化してからローカルの変更を書き込む。
4. 各ペルソナについて L1 検証を実施する。
5. `identity.yaml` を対象へマージする（既に存在し差分があれば停止して確認する）。
6. `growth.yaml` をエントリ単位でマージする。コンフリクトは `conflict_strategy`
   に従って処理する。
7. `derived_from` に同期の来歴（source、synced_at、direction: push）を追記する。
8. `--bank <name>` を使った場合、変更したペルソナのパスに対して
   `conclave-bank-sync --bank <name> --mode commit-push` を実行し、リモートへ
   commit・push する。
9. サマリレポートを出力する: ペルソナごとの追加/スキップ/要確認件数、および
   `--bank` を使った場合は commit/push の結果。

ユーザー入力: $ARGUMENTS
