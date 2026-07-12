---
description: 名前付きペルソナバンクのローカル git クローンを同期する（clone/pull、または commit+push）
argument-hint: "--bank <name> [--mode pull|commit-push] [--paths <path...>] [--message <text>]"
---

`conclave-bank-sync` スキルを使い、名前付きペルソナバンク（`.conclave/config.yaml`
の `sync.banks.<name>`）のローカルクローンに対して git 操作を実行する。通常は
`conclave-summon --bank` や `conclave-push-persona --bank` から内部的に呼ばれる。
バンクを手動で clone/更新したい場合や、失敗した push をリトライしたい場合に
直接実行する。

`skills/conclave-bank-sync/SKILL.md` のワークフローに従うこと:

1. `sync.banks.<name>` (リモート + ローカルパス) を解決する。見つからない場合は
   停止し、設定済みのバンク一覧を表示する。
2. `pull` モード（既定）: ローカルパスが存在しなければバンクを clone、既に
   存在すれば fast-forward pull する。未コミットのローカル変更や履歴の分岐が
   あれば停止する — 決して force しない。
3. `commit-push` モード: 指定された `--paths` のみをステージし、`--message` で
   コミット、push する。拒否された場合は rebase して最大3回リトライする。
   コンフリクトがあれば停止して報告する — 決して force-push しない。

Conclave を実行する環境に `git` CLI とリモートへのアクセス手段（SSH 鍵または
HTTPS 認証情報）が必要。

ユーザー入力: $ARGUMENTS
