---
description: retro が必要なタイミングで知らせる Conclave の SessionStart フックを導入する
argument-hint: "[scope: local|project]  (default: local = .claude/settings.local.json)"
---

Conclave の retro-due チェッカーを実行する Claude Code の `SessionStart` フックを
導入する。セッション開始のたびに `.conclave/config.yaml` と
`.conclave/retro/state.yaml` を確認し、週次/月次またはカウンタ方式の
レトロスペクティブが必要なときだけ `/conclave-retro` の実行を促す。それ以外は
無言で、`growth.yaml` 自体を編集することは決してない。

> **このコマンドが不要な場合。** Conclave が有効化済みの Claude Code プラグイン
> として（marketplace 経由などで）導入されている場合、同じフックは既に
> `hooks/hooks.json` に native で同梱されており自動的に有効になる。この状態で
> 本コマンドを実行すると、リマインドが二重登録されてしまう。本コマンドは
> 手動 clone や Codex 利用時、または自分の settings に明示的にフックを入れたい
> 場合にのみ使うこと。まず既存の設定に `conclave_retro_check.py` を含む
> コマンドがないか確認し、あれば「既に有効（native またはインストール済み）」
> と報告して停止する。

以下を正確に実行すること:

1. **フックスクリプトのパスを解決する。** この Conclave プラグイン内
   （`commands/` ディレクトリと同階層）にある `hooks/conclave_retro_check.py`
   を特定し、その絶対パスを使う。この環境で `${CLAUDE_PLUGIN_ROOT}` が
   設定されていれば `${CLAUDE_PLUGIN_ROOT}/hooks/conclave_retro_check.py`
   を優先する。ファイルの存在を確認する。

2. **インタプリタを選ぶ。** Windows では `python`、macOS/Linux では `python3`
   を使う。コマンド文字列を組み立てる:
   `<interpreter> "<absolute-path-to>/conclave_retro_check.py"`
   （スペースを含むパスでも動くよう引用符を残すこと）。

3. **設定ファイルを選ぶ**（`$ARGUMENTS` の `scope`、既定は `local`）:
   - `local` → `.claude/settings.local.json`（個人用・コミット対象外）
   - `project` → `.claude/settings.json`（リポジトリで共有）
   存在しなければ `{}` の内容で作成する。必要なら `.claude/` も作成する。

4. **フックを冪等にマージする**（既存の内容はすべて維持する）:
   - `hooks.SessionStart` が配列であることを保証する。
   - 既存の `SessionStart` エントリのいずれかが既に
     `conclave_retro_check.py` を含む `hooks[].command` を持つ場合、重複追加
     せず — そのコマンド文字列を新たに解決したパスへ更新し、「既にインストール
     済み（更新した）」と報告する。
   - それ以外は以下を追記する:
     ```json
     {
       "hooks": [
         { "type": "command", "command": "<interpreter> \"<abs-path>/conclave_retro_check.py\"" }
       ]
     }
     ```
   - JSON はインデント2スペースで書き戻す。他のキーやフックを削除・並び替え
     しないこと。

5. **報告する**: 設定ファイルのパス、インストールした正確なコマンド、そして
   このリマインドは retro が必要なときにのみ発火する旨（`.conclave/config.yaml`
   の `retro` ブロックで設定可能。`retro.auto: false` で無効化、または
   `/conclave-hook-uninstall` でフックを削除できる）。

補足:
- PATH 上に PyYAML を含む Python が必要（無い場合、スクリプトは無言で
  何もしない状態に縮退する）。
- このフックはリマインドのみを行う。実際の自動学習は `conclave-retro` スキルが
  小/大の変化度ゲートを伴って引き続き担う。

ユーザー入力: $ARGUMENTS
