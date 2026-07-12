---
name: conclave-retro
description: |
  Conclave のレトロスペクティブを実行し、ペルソナの成長メモリへ自動学習する。
  ユーザーが @conclave retro を求めたとき、retro トリガーが発火したとき
  （N回召喚後・大規模タスク後・週次/月次スケジュール）、またはペルソナが
  直近の勤怠を growth.yaml へ自己蒸留すべきときに使う。小さな改善は自己解釈
  のうえ自動で書き込み、大きな変更は人間承認待ちに回す。
---

# Conclave Retro

1体以上のペルソナに対して KPT 形式のレトロスペクティブを行い、その結果を
規模ゲートに従って**自動的に**成長メモリへ変換する。

これは `conclave-distill` / `conclave-distill-accept` の自動学習版に当たる。
`distill` が候補を提示して人間を待つだけなのに対し、`retro` は各ペルソナに
自分自身の解釈へ到達させ、小さく低リスクな学習を直接書き込ませる —
一方で、大きく持論を変える学習や機密性の高い学習は人間承認へエスカレー
ションする。

柱3（「持論は自分の言葉で解釈できる状態に到達して成立する」）は、各解釈を
**ペルソナ自身**がその声で記述することを要求することで維持される。候補の
文章をそのままコピーすることは受容とみなさない。

## いつ実行されるか

`retro` は次の3通りで呼び出される（すべて `.conclave/config.yaml` の
`retro` 配下で設定する）:

1. **N回召喚後** — `conclave-dismiss` がカウンタをインクリメントし、
   `retro.trigger_after_n_summons` に達すると、dismiss が出席したペルソナに
   対して retro を提案または自動実行する。
2. **大規模タスク後** — クローズしたセッションが大規模タスクと判定された
   場合（「大規模タスク判定」参照）、dismiss がその出席者に対して retro を
   トリガーする。
3. **スケジュールで** — `retro.schedule` に従い週次/月次で実行される。この
   MVP は手順ベースであるため、スケジュールはホスト側のスケジューラ
   （例: Claude Code の `/schedule` やフック）がこのスキルを呼び出すことで
   実現される。スキル自体は定期 retro が何をするかだけを定義する。

手動で呼び出す場合、明示的な `personas` リストや `scope`
（`since: <date>` または `last_n_sessions: <int>`）を受け付ける。

## 入力

（すべて任意。妥当な既定値を推測する）

- `personas`: retro を実行する対象ペルソナ id。既定値: 前回の retro 以降に
  新しい勤怠があった全員。
- `scope`: `since: <date>` または `last_n_sessions: <int>`。既定値: 各
  ペルソナの `last_retro_at` 以降の全て。
- `trigger`: `n_summons` | `big_task` | `schedule` | `manual`。記録用。
- `dry_run`: true の場合、`conclave-distill` のように振る舞う（提示のみ、
  何も書き込まない）。

## ワークフロー

1. `.conclave/config.yaml` を読む。`retro.auto` が false かつこれが手動呼び
   出しでない場合、停止し自動retroが無効であることを報告する。
2. 対象ペルソナとスコープを解決する。
3. 各ペルソナについて:
   1. `identity.yaml` と `growth.yaml` を読む。
   2. スコープ内の `.conclave/attendance/<persona-id>/*.yaml` と、文脈のため
      該当セッションの `minutes.md` を読む。`memory_seeds` と KPT の差分を
      集約する。
   3. `identity.yaml`（role・KPI・speech style）に根ざした、**ペルソナ自身の
      声による** KPT レトロスペクティブ（Keep / Problem / Try）を作る。
   4. 候補となる学習を導出する。各候補について、下記のゲートで規模を判定
      する。
   5. **小さな候補** → ペルソナが自分の解釈を書き、その学習は即座に
      `growth.yaml` に追記される（`conclave-distill-accept` の出力と同じ形）。
   6. **大きな候補** → `growth.yaml` には**触れない**。人間承認のため
      `conclave-distill-accept` 経由で承認されるよう
      `.conclave/retro/<retro-id>/pending.yaml` に追記する。
4. retro の記録を `.conclave/retro/retro-YYYYMMDD.md` に書き込む（下記
   「出力フォーマット」参照）。ファイル名には retro 実行日の日付を使う。
5. 各ペルソナの `last_retro_at` を更新し、`.conclave/retro/state.yaml` の
   召喚カウンタをリセットする。
6. 報告する: ペルソナごとに何が自動学習され、何が人間承認待ちか、そして
   変更した正確なファイル。

## state ファイル

`.conclave/retro/state.yaml` は周期とカウンタを追跡する。`conclave-dismiss`
がカウンタをインクリメントし、`conclave-retro` がそれをリセットして retro
日付を刻印し、SessionStart フック（`hooks/conclave_retro_check.py`）はこれを
読んでスケジュール済み retro が期限を迎えたかどうかを判断する。

```yaml
schema_version: "1.0"
last_retro_at: 2026-06-25        # グローバル、直近にいずれかの retro が実行された日
personas:
  <persona-id>:
    summons_since_retro: 0       # このペルソナの retro 後に 0 にリセット
    last_retro_at: 2026-06-25    # 任意、ペルソナごと
```

retro 実行後、グローバルおよびペルソナごとの `last_retro_at` を今日の日付
に設定し、対象となった各ペルソナの `summons_since_retro` を 0 にリセット
する。

## 規模ゲート（小 vs 大）

このゲートは、何を自動学習し何を人間待ちにするかを決める。既定のマッピングは
`config.yaml` の `retro.magnitude` にあり、以下のルールはその意図する意味論
である。

以下のいずれかを満たす候補は**大（BIG）**（人間承認が必要）:

- 既存の持論を覆す、上書きする、または実質的に狭める/広げる
  （`superseded_belief`、または変更された `updated_beliefs` エントリ）。
- その機密区分に対するセッションの既定を超える judgment/fact ライセンスを
  設定することになる（例えば judgment に対して `READ-ONLY` より広いもの、
  または `EXTERNAL-PUBLIC`/ギルド横断共有）。
- `CONFIDENTIAL` セッション由来であり、`PRIVATE` 以外のライセンスで
  書き込まれることになる。
- 他のペルソナの `READ-ONLY` judgment を、このペルソナ自身の持論として
  取り込む（ペルソナ間の持論移転）。
- 既存の `memory_entries` の解釈と矛盾する。

それ以外は**小（SMALL）**（自動学習）:

- 新しい fact と、矛盾しない初出の解釈。
- 既存の持論を覆すことなく精緻化する詳述。
- そのセッションの機密区分に対する既定ライセンスの範囲内。

判断に迷う場合は、その候補を大（BIG）として扱う。エスカレーションは安全だが、
持論変更の自動書き込みは安全ではない。

## 大規模タスク判定

以下のいずれかを満たす場合、クローズしたセッションを大規模タスクとして扱う
（`retro.big_task` の下で設定可能）:

- `meta.yaml` に `big_task: true` がある（人間による明示フラグ）。
- セッションが解決したトピック/保留事項が `retro.big_task.min_topics` 件以上。
- `confidentiality` が `CONFIDENTIAL`（既定でハイステークス扱い）。
- 勤怠に `superseded_belief` 候補が含まれる（持論が動いた）。

## 自動適用エントリの形式

小さな学習は `conclave-distill-accept` の出力と全く同じ形で `growth.yaml` に
追記され、自動適用されたことを示す来歴が付与される:

```yaml
memory_entries:
  - id: M-YYYYMMDD-NN
    fact:
      content: <何が起きたか>
      license: <機密区分に対する既定値>
      source: <session-id または retro-id>
      date: <date>
    judgment:
      persona: <persona-id>
      interpretation: <ペルソナ自身の言葉 — 候補のコピーではない>
      license: READ-ONLY
    provenance:
      via: retro
      retro_id: <retro-id>
      trigger: <n_summons|big_task|schedule|manual>
      magnitude: small
      auto_applied: true
```

## 保留エントリの形式

大きな学習はキューに入れられる（このスキルからは `growth.yaml` へ絶対に
書き込まない）:

```yaml
# .conclave/retro/<retro-id>/pending.yaml
schema_version: "1.0"
retro_id: <retro-id>
persona_id: <persona-id>
pending:
  - candidate: 1
    reason_big: <どのゲートルールに該当したか>
    fact: <内容>
    proposed_interpretation: <ペルソナの草案、人間の確認待ち>
    supersedes: <M-id または null>
    sources: [<勤怠ファイル>]
```

保留項目は後で `conclave-distill-accept`（人間が解釈を提供または確認する）
で解決する。

## 出力フォーマット

retro の記録は `.conclave/retro/retro-YYYYMMDD.md` に書き込む。
一目で読める、以下の最小テンプレートを使う — 密な文章にしない:

```markdown
# Retro — YYYY-MM-DD

## <persona-id>

**Keep**
- <うまくいったこと、1〜3項目>

**Problem**
- <うまくいかなかったこと、1〜3項目>

**Try**
- <次に試すこと、1〜3項目>

自動適用: <N>件 / 承認待ち: <N>件
```

ペルソナごとに1セクション。各 K/P/T は**3項目以内**に収める。
報告することが無いセクションは省略する。複数段落の説明文は書かない。

セッションログ（`.conclave/sessions/<id>/`）も同じ原則に従うべき: 箇条書き
中心・見出し最小、起きたことの文章による要約はしない —
minutes.md がそれ自体で語る。ログは構造を加えるだけにとどめる。

## ルール

- BIG 候補を `growth.yaml` に絶対に書き込まない。キューに入れる。
- 候補の文章を `interpretation` にそのままコピーしない。ペルソナが必ず
  言い直す。
- 既存の `memory_entries` を保持する。retro は追記のみ行う。新しい項目は
  `memory_entries:` リストの**中に**挿入し、ファイル末尾には追記しない —
  `growth.yaml` にはその後ろに `updated_beliefs:` ブロックがあることが多く、
  EOF 追記だと誤ったキーの下にネストしてしまう。
- fact と judgment を分離したままにし、機密区分の既定を尊重する。
- `retro.auto` が false の場合、`conclave-distill` のように振る舞う（提示のみ）。
- retro は判断材料であり、決定ではない。結果の所有権は常に人間にある。
- 根拠が薄い場合、疎な retro を書き、自動書き込みよりキュー入れを優先する。
