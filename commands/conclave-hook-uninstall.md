---
description: 設定から Conclave の SessionStart retro リマインドフックを削除する
argument-hint: "(no args)"
---

`/conclave-hook-install` が導入した Conclave の retro-due `SessionStart` フックを
削除する。設定のみを編集するもので、`hooks/conclave_retro_check.py` スクリプト
自体は削除せず、`.conclave/` データにも一切触れない。

以下を正確に実行すること:

1. **両方の設定ファイルを確認する**（存在する方のみ）:
   - `.claude/settings.local.json`
   - `.claude/settings.json`

2. **それぞれについて**、`hooks.SessionStart` 内で:
   - `conclave_retro_check.py` を含む `hooks[].command` を持つエントリを
     削除する。エントリが他の無関係なフックコマンドを束ねている場合は、
     一致する `command` オブジェクトのみを削除し、残りは維持する。
   - 空になったエントリオブジェクトを削除し、その結果 `hooks.SessionStart`
     が空配列になれば削除し、その結果 `hooks` が空オブジェクトになれば
     削除する。
   - 他の設定・フック・イベントタイプはすべてそのまま保持する。
   - 何か変更があった場合のみインデント2スペースで書き戻す。

3. **報告する**: 変更した設定ファイルと削除したコマンド、または削除対象が
   何もなかった場合は「Conclave のフックは見つからなかった」旨。
   `hooks/conclave_retro_check.py` はそのまま残っており、
   `/conclave-hook-install` で再度有効化できる旨も伝える。

ユーザー入力: $ARGUMENTS
