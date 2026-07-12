# Retrospective Auto-Learning (conclave-retro)

**版**: 1.0
**導入**: パッケージ v0.2.0 (skill) / v0.2.1 (native hook + marketplace)
**位置づけ**: MVP Spec の蒸留機構 (§5.3 / §5.4) を拡張する。MVP Spec / 完成版
Spec / 全体概要 Spec の下位文書。
**根拠**: 柱3 (持論は自分の言葉で解釈できて成立) を保ったまま「使うほど育つ」を
実現するための拡張。

---

## 1. 何を解決するか

`conclave-distill` / `conclave-distill-accept` は、人間が一件ずつ解釈到達を確認して
受け入れる **手動ルート** である (柱3 の厳格実装)。これは安全だが、運用負荷が高く、
「使えば使うほど自動で賢くなる」体験にはならない。

`conclave-retro` は、ペルソナ自身が KPT レトロスペクティブを行い、学びを
`growth.yaml` に **自動反映する** 拡張ルートである。柱3 は「**自分** (= ペルソナ) の
言葉で解釈できて成立」と読み替えることで保たれる。候補テキストのコピーは受け入れ
ではなく、ペルソナが自分の言葉で言い直すことを必須とする。

「自動で全部書く」のではなく、**内容の大きさで人間関与を分ける** のが核心である。

---

## 2. magnitude ゲート (柱3 の保全)

各学習候補を「小さい / 大きい」に分類し、扱いを変える。

### 2.1 小さな改善 (自動適用)

ペルソナが自分の言葉で解釈を書き、`growth.yaml` に即追記する。

- 新しい事実 + 矛盾しない初回解釈
- 既存持論を反転させない補強・精緻化
- 機密分類のデフォルトライセンス内

### 2.2 大きな変更 (人間承認)

`growth.yaml` には書かず、`.conclave/retro/<retro-id>/pending.yaml` に退避する。
後で `conclave-distill-accept` で人間が承認する。

- 既存持論の反転・上書き・大幅な拡縮 (`superseded_belief` / `updated_beliefs` 変更)
- 機密分類デフォルトを超えるライセンス格上げ (judgment が READ-ONLY より広い、
  EXTERNAL-PUBLIC、別ギルド共有など)
- `CONFIDENTIAL` セッション由来で PRIVATE 以外のライセンス
- 他ペルソナの READ-ONLY judgment を自分の持論として取り込む (持論の越境移植)
- 既存 `memory_entries` の解釈と矛盾する

**迷う候補は大きい扱い** にする (安全側へ倒す)。格上げは安全だが、stance 変更の
自動書き込みは危険。

デフォルトのマッピングは `.conclave/config.yaml` の `retro.magnitude` に置く。

---

## 3. 発火トリガー

`.conclave/config.yaml` の `retro` ブロックで制御する。

| トリガー | 仕組み |
|---|---|
| N 回召喚ごと | `conclave-dismiss` が `state.yaml` のカウンタを進め、`retro.trigger_after_n_summons` 到達で発火 |
| 大きなタスク後 | 召喚時 `meta.yaml` に `big_task: true`、論点数 >= `retro.big_task.min_topics`、または `CONFIDENTIAL` セッションを大タスクと判定し dismiss 時に発火 |
| 週次 / 月次 | `retro.schedule`。手順書ベースのため実タイマーはホスト側 (SessionStart フック / `/schedule`) が `conclave-retro` を呼んで実現 |

`retro.auto: false` のとき、retro は `conclave-distill` と同じく候補提示のみに退化する。

---

## 4. SessionStart フック (週次 / 月次の自動リマインド)

`hooks/conclave_retro_check.py` を Claude Code の `SessionStart` フックとして登録すると、
セッション開始時に `config.yaml` と `state.yaml` を読み、レトロ期限が来た時だけ
`/conclave-retro` の実行を促す。期限外・`.conclave/` 無し・`retro.auto:false` では無言。

- 配布形態: `hooks/hooks.json` として plugin に同梱 (native)。marketplace /
  有効化済み plugin では自動で効く。`${CLAUDE_PLUGIN_ROOT}` でスクリプトを解決。
- 手動 clone / Codex 用に `/conclave-hook-install` / `/conclave-hook-uninstall`
  コマンドも提供 (二重通知を避けるため native と併用しない)。
- フックは判定とリマインドのみ。`growth.yaml` は決して書かない (実学習は
  `conclave-retro`)。

---

## 5. データ契約

### 5.1 state.yaml

`.conclave/retro/state.yaml`。`conclave-dismiss` が更新、`conclave-retro` が
リセット、フックが読む。

```yaml
schema_version: "1.0"
last_retro_at: 2026-06-25        # 全体、最後に retro した日
personas:
  <persona-id>:
    summons_since_retro: 0       # retro 後 0 にリセット
    last_retro_at: 2026-06-25    # 任意、ペルソナ別
```

### 5.2 自動適用エントリ (growth.yaml)

`conclave-distill-accept` と同形 + `provenance` を付与。**`memory_entries:` リストへ
挿入** すること (ファイル末尾追記は後続の `updated_beliefs:` 配下に誤ってネストする)。

```yaml
memory_entries:
  - id: M-YYYYMMDD-NN
    fact: { content: ..., license: ..., source: ..., date: ... }
    judgment:
      persona: <persona-id>
      interpretation: <ペルソナ自身の言葉。候補のコピー不可>
      license: READ-ONLY
    provenance:
      via: retro
      retro_id: <retro-id>
      trigger: n_summons | big_task | schedule | manual
      magnitude: small
      auto_applied: true
```

### 5.3 pending.yaml (承認待ち)

```yaml
# .conclave/retro/<retro-id>/pending.yaml
schema_version: "1.0"
retro_id: <retro-id>
persona_id: <persona-id>
pending:
  - candidate: 1
    reason_big: <マッチしたゲート規則>
    fact: <内容>
    proposed_interpretation: <ペルソナ草案。人間が確認・確定>
    supersedes: <M-id or null>
    sources: [<attendance files>]
```

### 5.4 retro 記録

`.conclave/retro/<retro-id>/retro.md` に KPT・自動適用分・承認待ち分・出典を残す。

---

## 6. 設計原則との整合

| 原則 | 整合 |
|---|---|
| 柱3 (解釈到達で成立) | ペルソナ自身が自分の言葉で解釈。コピー禁止。大きな変更は人間へ |
| 柱2 (個性 = 解釈の差) | judgment は READ-ONLY のまま、持論越境は人間承認 |
| A2 防御 (誘導が鬱陶しい) | フックは期限時のみ・無言 no-op、`retro.auto:false` で停止可 |
| A4 防御 (機密漏洩) | CONFIDENTIAL 由来やライセンス格上げは自動適用しない |
| 根本宣言 (支援機構) | retro は判断材料。最終判断と責任は人間 |

---

## 7. 関連

- 操作手順: [usage.md](usage.md) §7b
- skill 本体: `skills/conclave-retro/SKILL.md`
- 蒸留 (手動ルート): MVP Spec §5.3 / §5.4
- 撤退条件: [../ops/withdrawal-criteria.md](../ops/withdrawal-criteria.md)
