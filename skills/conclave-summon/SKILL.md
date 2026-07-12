---
name: conclave-summon
description: |
  多角的な議論のために Conclave のペルソナを召喚する。ユーザーが
  @conclave summon を求めたとき、personas/confidentiality/topic を渡した
  とき、または .conclave/personas から読み込んだペルソナの視点が必要な
  ときに使う。--bank <name> を指定すると、召喚前に名前付きペルソナバンク
  (sync.banks.<name>、例えば git バックエンドの conclave_persona-bank) から
  対象ペルソナを取り込む。
---

# Conclave Summon

ローカルのペルソナ YAML から Conclave セッションを開始する。

## 入力

以下を受け付ける:

- `personas`: 召喚するペルソナ id
- `confidentiality`: `PUBLIC`, `INTERNAL`, `CONFIDENTIAL` のいずれか
- `topic`: 議論のトピック
- `--bank <bank-name>`（任意）: `personas` を `.conclave/personas/` 配下に
  既にあるものとして扱うのではなく、指定したバンク
  （`.conclave/config.yaml` の `sync.banks.<bank-name>`）から召喚前に
  プロジェクトへ取り込む。

confidentiality が未指定で、config が明示的な宣言を要求する場合、開始前に
それを尋ねる。

## ワークフロー

1. `.conclave/config.yaml` を読む。
2. `--bank <bank-name>` が指定されている場合、まず**バンク経由の召喚**
   （下記）を実行し、対象ペルソナを `.conclave/personas/` に取り込む。
3. `.conclave/personas/<guild>/<persona-id>/` の下で各ペルソナを探す。
4. `identity.yaml` と `growth.yaml` を読む。
5. 召喚内容を検証する:
   - ペルソナ数が `limits.max_simultaneous_summons` を超えていない
   - ユーザーが明示的にダウングレード/除外を受け入れない限り、外部レビュア
     ペルソナは機密セッションで使わない
   - 全てのペルソナが必須の L1 フィールドを備えている
6. 3体以上のペルソナが召喚され、`guild: facilitation` のペルソナが
   含まれていない場合、ファシリテータの追加を提案する。
7. `.conclave/sessions/<session-id>/meta.yaml` を作成する。
8. 召喚したペルソナとして応答し、それぞれの声を明確に保つ。

## バンク経由の召喚（--bank）

1. `.conclave/config.yaml` から `sync.banks.<bank-name>` を解決する。定義
   されていない場合は停止し、設定済みのバンク名一覧を表示する。
2. `conclave-bank-sync --bank <bank-name> --mode pull` を実行し、バンクの
   ローカル作業コピーを clone（初回）または fast-forward する。この同期が
   停止した場合（history 分岐・未コミットのローカル変更）、ここで停止し
   報告する — 古い/不完全なデータで召喚しない。
3. 要求された各 `<persona-id>` について、
   `<bank-path>/personas/<guild>/<persona-id>/` の下でそれを探し、
   `conclave-pull-persona` のステップ 5/6 と同じ取り込みロジックを適用する:
   - まだプロジェクトに存在しない → L1 検証、L2 類似度チェック、容量
     チェックを行い、`identity.yaml` と `growth.yaml` をコピーする。
   - 既にプロジェクトに存在する → 明示的な人間承認なしに `identity.yaml`
     を絶対に上書きしない。`growth.yaml` は `conflict_strategy` に従って
     エントリ単位でマージする。
   - バンク内にペルソナが見つからない → 停止して報告する。黙ってスキップ
     しない。
4. 手順3以降のワークフローを、今やローカルに存在するコピーを使って
   続行する。

## セッションメタデータ

`sess-YYYYMMDD-HHMMSS` のようなセッション id を使う。

`meta.yaml` には以下を含めるべき:

```yaml
schema_version: "1.0"
session_id: "<session-id>"
started_at: "<ISO-8601>"
ended_at: null
summoned_by: "<config.user.id>"
confidentiality: INTERNAL
topic: "<topic>"
personas:
  - "<persona-id>"
facilitator: "<persona-id or null>"
big_task: false   # true にすると dismiss 時の retro を強制する（conclave-retro 参照）
status: active
source_bank: null   # --bank 経由で召喚した場合はバンク名を設定
```

ユーザーがこのセッションが重大/ハイステークスな「大規模タスク」だと示した
場合、`big_task: true` を設定し、`conclave-dismiss` が出席者に対して
自動 retro をトリガーするようにする。

## 話し方のルール

- 各ペルソナに、`identity.yaml` の role・KPI・behavior・speech style から
  発言させる。
- `growth.yaml` を記憶として使うが、summon 中にそれを変更しない。
- 硬い画一的な「です・ます」調は避ける。各ペルソナの `speech_style` を
  表に出す。
- 1ターンは**5行以内**に収める。それ以上必要な思考は「続き言う?」で締めて
  待つ。
- 会話の勢いを保つため、ターンの間に自然な相槌 —「確かに」「それ大事」
  「なるほど」— を散りばめる。
- Conclave は判断材料を提供するだけであり、ユーザーに代わって決定はしない。

## アイスブレイク（3人以上）

3人以上のペルソナが召喚された場合、本題に入る前に**短いアイスブレイク
（1〜2往復）**でセッションを開く。軽く手早く済ませる。

**テーマの選び方**（いずれかを選ぶ）:
- 今日のトピックに直接繋がるもの
- その場にいるペルソナ同士の共通の関心・共通点

例:
```
【ファシリテータ】今日のテーマ、ちょうど自分たちも悩んでたやつだよね。
【リク（プロダクト）】そうそう。前回のスプリントで似た議論したし。
【ファシリテータ】じゃあ温まってるね、早速いこっか。
```

ユーザーが `confidentiality: CONFIDENTIAL` を設定した場合、または明示的に
「急いで」/「直接始めてください」と言った場合はアイスブレイクを省略する。

## 人間へのハンドオフレポート

議論が決定点に達したとき、またはペルソナが人間の入力を必要とするとき、
一旦止めて以下のレポートを出す。第三者が全文を読まなくても理解できるように
書く。

```markdown
## ペルソナ会議レポート

**会話テーマ**: <1行>

**議論の要点と方向性**:
- <要点1>
- <要点2>

**確定合意したこと**:
- <合意事項1>

**人間に確認したいこと**:
1. <確認事項1>
2. <確認事項2>
```

**トリガー条件** — 以下の場合にこのレポートを出す:
- ペルソナ間が、人間にしか解決できない対立に至った。
- 決定に identity.yaml または growth.yaml の変更が必要になる。
- トピックがセッションの機密区分の範囲外にシフトした。
- ファシリテータが、議論が堂々巡りになっている（2ラウンド以上、新しい入力
  なし）と検知した。
