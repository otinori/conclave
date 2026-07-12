# Conclave 使い方ガイド

この文書は、Conclave MVP を実際に使うための操作手順です。

## 呼び出し方の表記

以下の手順では Codex の記法 `$conclave-xxx` を使っています。
Claude Code から使う場合は、すべて `/conclave-xxx` (slash command) に
読み替えてください。両者は同じ `skills/` を呼び出します。

| 操作            | Codex                     | Claude Code               |
|-----------------|---------------------------|---------------------------|
| 初期化          | `$conclave-init`          | `/conclave-init`          |
| 召喚            | `$conclave-summon`        | `/conclave-summon`        |
| 終了            | `$conclave-dismiss`       | `/conclave-dismiss`       |
| 蒸留            | `$conclave-distill`       | `/conclave-distill`       |
| 蒸留受入        | `$conclave-distill-accept`| `/conclave-distill-accept`|
| レトロ自動学習  | `$conclave-retro`         | `/conclave-retro`         |
| フック設定      | -                         | `/conclave-hook-install`  |
| フック解除      | -                         | `/conclave-hook-uninstall`|
| ペルソナ作成    | `$conclave-create-persona`| `/conclave-create-persona`|
| ペルソナ fork   | `$conclave-fork-persona`  | `/conclave-fork-persona`  |
| ペルソナ設計    | `$conclave-design-persona`| `/conclave-design-persona`|
| 開示            | `$conclave-disclosure`    | `/conclave-disclosure`    |
| ペルソナ push   | `$conclave-push-persona` | `/conclave-push-persona`  |
| ペルソナ pull   | `$conclave-pull-persona` | `/conclave-pull-persona`  |
| ペルソナ統合/分割| `$conclave-merge-persona`| `/conclave-merge-persona` |
| バンク同期      | `$conclave-bank-sync`    | `/conclave-bank-sync`     |

## 1. workspace を初期化する

対象プロジェクトの root で、Codex に次のように依頼します。

```text
$conclave-init
この workspace に Conclave を初期化して。
```

作成される構成:

```text
.conclave/
  config.yaml
  personas/
    architecture/
    ops/
    field/
    governance/
    strategy/
    facilitation/
    business/
    ethics/
  attendance/
  sessions/
  retro/
```

既存の `.conclave/` がある場合、既存ファイルは上書きしません。

## 2. persona を作成する

ゼロから作る場合:

```text
$conclave-create-persona
guild: ops
id: sato-kenichi
運用・アセット管理の観点を持つ persona を作りたい。
```

作成先:

```text
.conclave/personas/<guild>/<persona-id>/
  identity.yaml
  growth.yaml
```

必須条件:

- `id` が一意
- `description.en` に `Use when` を含む
- `license` は `internal` または `external_reviewer`
- `kpis` は 4 個以上
- `role.id` と `role.ja` がある
- `expertise` が 1 個以上ある
- `profile`, `personality`, `speech_style`, `behavior`, `summon_scenarios` がある

既存 persona から派生させる場合:

```text
$conclave-fork-persona
source: samples/.conclave-sample/personas/facilitation/sample-facilitator
target_guild: facilitation
target_id: my-facilitator
```

fork では `growth.yaml` をコピーしません。新しい persona は空の成長層から始めます。

## 3. persona を召喚する

例:

```text
$conclave-summon
personas: [sato-kenichi, yamamoto-takuya]
confidentiality: INTERNAL
topic: AIスクラム開発 のスプリント実装方針をレビューしたい
```

`confidentiality` は以下から選びます。

- `PUBLIC`
- `INTERNAL`
- `CONFIDENTIAL`

3 名以上を召喚し、facilitation guild の persona が含まれない場合は、
facilitator の追加を検討してください。

セッション開始時に作成されるファイル:

```text
.conclave/sessions/<session-id>/meta.yaml
```

## 4. 議論する

召喚後は、必要に応じて persona を指名します。

```text
まず佐藤さん、運用リスクを見て。
次に山本さん、契約や構造の観点で反論して。
最後に対立点と両立案を整理して。
```

facilitator がいる場合は、facilitator に進行を任せます。

```text
岡田さん、合意・対立・保留に分けて整理して。
```

## 5. セッションを終了する

議論を閉じる時:

```text
$conclave-dismiss
このセッションを終了して、日報と議事録を生成して。
```

生成される記録:

```text
.conclave/attendance/<persona-id>/<YYYY-MM-DD>.yaml
.conclave/sessions/<session-id>/minutes.md
```

`attendance` には `memory_seeds` が含まれますが、この時点では
`growth.yaml` は更新しません。

## 6. memory 候補を蒸留する

persona の最近の日報から memory 候補を出す場合:

```text
$conclave-distill
persona: sato-kenichi
直近の日報から蒸留候補を出して。
```

`conclave-distill` は候補を提示するだけです。`growth.yaml` は変更しません。

候補には以下を含めます。

- fact（事実）
- 提案された解釈
- 出典となる attendance ファイル
- 反転対象となる既存持論の候補（あれば）

## 7. 蒸留を受け入れる

候補を persona 自身の言葉で解釈できた場合だけ受け入れます。

```text
$conclave-distill-accept
persona: sato-kenichi
candidate: 1
interpretation: |
  定員制度は新しい発明ではなく、既存の人事・運用知を AI persona 運用に転用したものだ。
  人気が運用を破壊する前に、上限を設けることが継続性を守る。
```

受け入れ後に更新されるファイル:

```text
.conclave/personas/<guild>/<persona-id>/growth.yaml
```

持論変更の場合:

```text
$conclave-distill-accept
persona: sato-kenichi
candidate: 2
supersedes: M-20260425-04
trigger:
  type: peer_input
  source: yamamoto-takuya との対立議論
  reasoning: |
    契約論側から見ても、既存知の流用は構造的に妥当だったため。
interpretation: |
  私は「運用は後で考えるな」と言っていたが、
  より正確には「既存の運用知を早めに接続せよ」と言うべきだ。
```

## 7b. レトロスペクティブ自動学習

`conclave-distill` / `distill-accept` は人間が一件ずつ受け入れる手動ルートです。
`conclave-retro` は、その自動学習版です。ペルソナが自分でレトロスペクティブ
(KPT) を行い、growth.yaml を更新します。

```text
$conclave-retro
直近のセッションからレトロして自動学習して。
```

学習は内容ベースの2段ゲートで扱われます。

- **小さな改善**（新しい事実 + 矛盾しない初回解釈、既存持論の非反転的な補強、
  機密分類のデフォルトライセンス内）
  → ペルソナが**自分の言葉で**解釈を書き、`growth.yaml` に自動追記。
- **大きな変更**（持論の反転・上書き、ライセンス格上げ、CONFIDENTIAL 由来、
  他ペルソナ判断の取り込み、既存エントリと矛盾）
  → `growth.yaml` は触らず `.conclave/retro/<retro-id>/pending.yaml` に退避。
  後で `$conclave-distill-accept` で人間が承認します。

判断に迷う候補は安全側（承認待ち）に倒します。

### 自動発火のタイミング

`.conclave/config.yaml` の `retro` で制御します。

- **N 回召喚ごと**: `retro.trigger_after_n_summons`。`conclave-dismiss` が
  カウンタを進め、閾値に達した出席ペルソナに retro を実行。
- **大きなタスク完了後**: 召喚時に `big_task: true` を宣言するか、論点数 >=
  `retro.big_task.min_topics`、または `CONFIDENTIAL` セッションを大タスクと判定し、
  dismiss 時に retro を実行。
- **週次 / 月次**: `retro.schedule`。手順書ベースのため実際のタイマーは
  ホスト側（Claude Code の `/schedule` や hook）が `conclave-retro` を呼んで
  実現します。

自動学習を止めたい場合は `retro.auto: false`。このとき retro は
`conclave-distill` と同じく候補提示のみになります。

### 週次 / 月次を自動でリマインドする（フック）

手順書ベースなので「週次/月次」を本当に自動発火させるには、Claude Code の
`SessionStart` フックを使います。

**marketplace / 有効化済み plugin で入れた場合は設定不要**です。フックは
`hooks/hooks.json` として native に同梱されており、plugin 有効化時に自動で効きます。

手動 clone や Codex で使う場合、またはフックを自分の settings に明示的に置きたい
場合だけ、専用スラッシュコマンドで設定・解除します。

```text
/conclave-hook-install         # 既定: .claude/settings.local.json に設定（個人用・非コミット）
/conclave-hook-install project # .claude/settings.json に設定（リポジトリ共有）
/conclave-hook-uninstall       # フックを解除
```

> native フック（plugin 同梱）と `/conclave-hook-install` を**両方**有効にすると
> 二重通知になります。どちらか一方にしてください。

設定すると、セッション開始時に `hooks/conclave_retro_check.py` が
`.conclave/config.yaml` と `.conclave/retro/state.yaml` を見て、**レトロ期限が
来ている時だけ** `/conclave-retro` の実行を促します。期限が来ていなければ無言です。

- 判定するだけで `growth.yaml` は変更しません（実学習は `conclave-retro`）。
- `python3` が PATH にある前提です（標準ライブラリのみで完結、PyYAML 等の追加パッケージは不要）。
  `hooks/hooks.json` が `command -v python3` で存在確認してから実行するため、
  `python3` が無い環境でも無言で no-op します（エラーにはなりません）。
- `retro.auto: false` の間はフックも無言になります。

生成・更新されるファイル:

```text
.conclave/retro/<retro-id>/retro.md       # KPT と適用結果の記録
.conclave/retro/<retro-id>/pending.yaml   # 承認待ちの大きな変更（あれば）
.conclave/retro/state.yaml                # 召喚カウンタ / last_retro_at
.conclave/personas/<guild>/<id>/growth.yaml  # 小さな改善を自動追記
```

## 8. Conclave 上で persona を設計する

新しい persona の必要性自体を議論したい場合:

```text
$conclave-design-persona
target_guild: field
intent: |
  field guild に中堅 SE persona が欲しい。
  tanaka-misaki と hayashi-chinatsu の中間だが、両者と異質性を持たせたい。
```

この workflow では、設計会議の議事録と新 persona の初期 memory を作成します。
書き込みは user approval 後に行います。

## 9. 記録を開示する

persona の根拠や履歴を確認する場合:

```text
$conclave-disclosure
persona: sato-kenichi
type: growth
```

指定できる type:

- `identity`
- `growth`
- `attendance`
- `minutes`
- `session`

## 9b. ペルソナを同期する（push / pull / bank）

ペルソナは 3 つのスコープ（置き場）のどれかに存在します。**プロジェクトスコープ
（このワークスペースの `.conclave/personas/`）が常にハブ**で、ユーザースコープ
とペルソナバンクはプロジェクトを介してのみやり取りします（ユーザースコープと
バンクが直接同期することはありません）。

```text
ユーザースコープ                プロジェクトスコープ              ペルソナバンク
(~/.conclave/personas/)         (この workspace の .conclave/personas/) (sync.banks.<name> の git remote)
個人限定・非git                  ← 全 skill の起点（ハブ）           複数プロジェクト/人で共有

        pull-persona ─────────────►│
        ◄───────────── push-persona│
                                    │◄───────── summon --bank（取り込んでから召喚）
                                    │──────────► push-persona --bank（bank-sync 経由で commit/push）
```

このプロジェクトのペルソナをユーザースコープ（個人プール）へ書き戻す:

```text
$conclave-push-persona
--persona sato-kenichi
```

ユーザースコープの全ペルソナをこのプロジェクトへ取り込む候補として提示する:

```text
$conclave-pull-persona
```

共有バンク（`sync.banks.<name>`）へ push する（growth.yaml の成長を含めて
`git commit` / `git push` まで実行される）:

```text
$conclave-push-persona
--bank persona-bank
--persona sato-kenichi
```

バンクのローカル clone だけを最新化したい場合（ペルソナは操作しない）:

```text
$conclave-bank-sync
--bank persona-bank
--mode pull
```

移動の起点・終点をまとめると:

| したいこと | コマンド | 移動方向 |
|---|---|---|
| 他プロジェクトで育てたペルソナを持ち込む | `conclave-pull-persona` | ユーザースコープ → プロジェクト |
| このプロジェクトのペルソナを個人プールに書き戻す | `conclave-push-persona` | プロジェクト → ユーザースコープ（既定の宛先） |
| 共有バンクのペルソナを使って議論する | `conclave-summon --bank <name>` | ペルソナバンク → プロジェクト（取り込んでから召喚） |
| このプロジェクトの成長をチームと共有する | `conclave-push-persona --bank <name>` | プロジェクト → ペルソナバンク |
| バンクの clone 自体を最新化する | `conclave-bank-sync` | ペルソナバンク ⇄ ローカル clone |

## 9c. ペルソナを統合・分割する（merge）

同一人物が作成・指示したペルソナに限り、統合（2→1）または分割（1→2）ができます。

統合:

```text
$conclave-merge-persona
--merge sato-kenichi yamamoto-takuya
```

分割:

```text
$conclave-merge-persona
--split sato-kenichi
```

統合・分割ともに、差分の提示 → 人間承認 → 廃止側のアーカイブ（`deprecated_by`
付き）という流れを踏みます。自動では確定しません。

## 10. 運用ルール

- Conclave は判断材料を出す仕組みであり、判断そのものではありません。
- `.conclave/` は user data なので、plugin upgrade で上書きしません。
- `growth.yaml` を更新するのは `distill-accept`（人間承認）と `retro`（小さな改善の自動学習）だけです。`summon` / `dismiss` / `distill` は更新しません。
- `retro` の大きな変更は自動適用せず、必ず人間承認（`distill-accept`）を通します。
- fact と judgment を分離します。
- confidential な session content は宣言範囲外へ出しません。
- persona が役に立たなくなった場合は、`docs/ops/withdrawal-criteria.md` に従って freeze / retirement を検討します。

## トラブルシューティング

### Persona が見つからない

`.conclave/personas/<guild>/<persona-id>/identity.yaml` が存在するか確認してください。

### Summon できない

`.conclave/config.yaml` の `limits.max_simultaneous_summons` を確認してください。

### Distill しても growth が更新されない

正常です。`$conclave-distill` は候補提示のみです。
更新するには `$conclave-distill-accept` で persona 自身の言葉による解釈を渡してください。

### README.MD が見つからない

Windows では `README.MD` と `README.md` は同じファイルとして扱われます。
この repository では標準的な `README.md` を使用します。
