---
name: conclave-bank-sync
description: |
  名前付きペルソナバンク (config.yaml の sync.banks.<name>) 向けの git 連携。
  未 clone なら clone、最新状態への pull、ローカル変更の commit+push を行う。
  conclave-summon --bank と conclave-push-persona --bank から内部的に使われる。
  ペルソナを操作せずバンクだけを同期する用途で単体実行することもできる。
---

# Conclave Bank Sync

`.conclave/personas/` はプロジェクトローカルなデータだが、`sync.banks.<name>` に
登録された名前付きバンクは **git リモートを持つ共有ディレクトリ**として扱う。
conclave 自体はサーバーや MCP 通信を持たない設計のため、リモートへの反映は
このスキルが `git` CLI をローカルの作業ディレクトリ（バンクの clone）に対して
実行することでのみ行う。**`git` CLI とリモートへのアクセス権限（SSH 鍵 /
HTTPS 資格情報）がある環境が前提**になる。

## 入力

- `--bank <bank-name>`: 対象バンク名（`sync.banks.<bank-name>` に定義されている必要がある）
- `--mode pull|commit-push`（省略時 `pull`）
- `commit-push` モードのみ:
  - `--paths <path...>`: バンク clone 内でステージする相対パス（例:
    `personas/product/riku`）。呼び出し元（push-persona）が変更したペルソナ
    ディレクトリのみを渡す。
  - `--message <text>`: コミットメッセージ

## ワークフロー — mode: pull

1. `sync.banks.<bank-name>` を `.conclave/config.yaml` から解決する。無ければ
   停止し、設定済みバンク一覧を提示して終了する。
2. `<path>` が存在しない場合: `git clone <remote> <path>` を実行する（初回同期）。
3. `<path>` が存在する場合:
   - `git -C <path> status --porcelain` でローカルに未コミットの変更が無いことを確認する。
     ある場合は停止し、内容を報告する（自動 stash/破棄はしない）。
   - `git -C <path> pull --ff-only` を実行する。
   - fast-forward できない（history が分岐している）場合は停止し、人間に
     `<path>` での手動解決を依頼する。force pull は行わない。
4. 完了したら clone パスと直前コミット SHA を報告する。

## ワークフロー — mode: commit-push

呼び出し元（`conclave-push-persona --bank`）が先に **mode: pull** を実行し、
その後バンク clone 内のファイルを書き換えていることが前提。

1. `git -C <path> status --porcelain -- <paths>` で対象パスに実際の差分が
   あるか確認する。差分が無ければ「変更なし」を報告して終了する。
2. `git -C <path> add -- <paths>`（渡された persona ディレクトリのみ。
   無関係な変更は add しない）。
3. `git -C <path> commit -m "<message>"`。
4. `git -C <path> push`。
5. push が reject された場合（リモートが進んでいる = 他プロジェクトが先に
   push した）:
   - `git -C <path> pull --rebase` → 再度 `git -C <path> push` を最大 3 回まで
     自動リトライする。
   - 3 回失敗した場合、または rebase 中に conflict が発生した場合は停止し、
     `<path>` の状態をそのまま人間に報告する（自動で conflict を解決しない）。
6. 成功したら commit SHA と push 先ブランチを報告する。

## ルール

- Force push (`--force` / `--force-with-lease`) は行わない。
- commit-push モードで `add` するのは呼び出し元が明示した persona パスのみ。
  バンク clone 内の無関係な変更を巻き込まない。
- pull で history が分岐している、または commit-push で rebase が
  conflict した場合は必ず停止し、人間の判断を待つ（`conflict_strategy` に
  関わらず、git レベルの conflict は常に human-in-the-loop）。
- Conclave は判断材料を提供するだけであり、ユーザーに代わって決定はしない。
