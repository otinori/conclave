# Conclave のインストール

Conclave は Codex と Claude Code の両方に同じ engine (`skills/` + `templates/`) で
インストールできます。それぞれの plugin manifest だけが分かれています。

## 必要環境

- ローカル plugin に対応した Codex、**または** ローカル plugin に対応した Claude Code
- `.conclave/` ユーザーデータを作成できるプロジェクト workspace

## Codex へのインストール

このリポジトリのルートを plugin フォルダとして使います。plugin manifest は:

```text
.codex-plugin/plugin.json
```

インストール後、Conclave の skills は以下から利用できます:

```text
skills/
```

Codex から呼び出すときは `$conclave-init` のように先頭に `$` を付けます。

## Claude Code へのインストール

このリポジトリのルートを plugin フォルダとして使います。plugin manifest は:

```text
.claude-plugin/plugin.json
```

インストール後、以下が利用できます:

```text
skills/           # 自動起動される skills
commands/         # /conclave-init, /conclave-summon, ...
hooks/hooks.json  # retro リマインドの native SessionStart フック（自動有効化）
```

Claude Code から呼び出すときは `/conclave-init` のように slash command として打つか、
自然文で依頼してください (skill の description にマッチすると自動で呼び出されます)。

### Plugin marketplace 経由でインストールする (推奨)

この repo は自分自身を 1 plugin として配る marketplace になっています
(`.claude-plugin/marketplace.json`)。Claude Code から:

```text
/plugin marketplace add otinori/conclave
/plugin install conclave@conclave
```

(`owner/repo` 形式・git URL・ローカルパスのいずれでも `marketplace add` できます。)

インストールして plugin を有効化すると、engine skills・slash commands に加えて
**retro リマインドの SessionStart フックが native に自動で有効化**されます
(`hooks/hooks.json` が `${CLAUDE_PLUGIN_ROOT}/hooks/conclave_retro_check.py` を呼ぶ)。
フックはレトロ期限が来た時だけ通知し、`.conclave/` の無い workspace では無言です。

> marketplace / enabled plugin 経由で入れた場合、フックは既に native です。
> `/conclave-hook-install` を重ねて実行しないでください (二重通知になります)。
> `/conclave-hook-install` は手動 clone や Codex 用のフォールバックです。

検証は `claude plugin validate .` で行えます。

## Workspace の初期化

対象プロジェクト workspace で、エージェントに `conclave-init` を使うよう依頼します。

- Codex: `$conclave-init`
- Claude Code: `/conclave-init`

初期化により以下が作成されます:

```text
.conclave/
  config.yaml
  personas/
  attendance/
  sessions/
  retro/
```

既存の `.conclave/` 配下のファイルはユーザーデータです。plugin のアップグレード時に上書きしないでください。

## アップグレード時のルール

Plugin のアップグレードは `skills/`, `commands/`, `templates/`, `docs/`, `samples/` を
置き換えることがあります。ユーザーが明示的に移行を求めない限り、workspace の
`.conclave/` ディレクトリを変更してはいけません。
