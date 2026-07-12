# Conclave MVP Spec — Skills版（マーケット配布前提・ローカル完結）

**版**: 2.0
**作成日**: 2026-04-26
**対象**: Phase α（個人ツール検証）
**実装基盤**: Claude Skills プラグイン（マーケット配布前提）
**前提**: 全体概要 Spec を読了済み

**v1.0からの変更**: マーケット配布前提に再設計。配布物（エンジンSkills）とユーザーデータ（`.conclave/`）を完全分離。ペルソナ定義をYAML化。ギルド軸グルーピング。

---

## 1. MVPの目的とスコープ

### 1.1 目的

Conclave 構想を**コードを書かずに**動かし、思想として機能していることを実証する。**最初からマーケット配布可能な形で構築**することで、Phase α 検証後そのまま Phase β（複数ユーザーへの展開）に移行できる。

### 1.2 配布モデル

**「エンジンのみ配布、ペルソナはユーザー独自作成」**（全体概要 Spec §12 3層スコープ分離）

```
┌────────────────────────────────────┐
│  配布物（Claude Skills マーケット）    │
│  - Conclaveエンジン Skills          │
│  - テンプレート                       │
│  - ドキュメント                       │
│  - 最小サンプル（参照用）              │
└────────────────────────────────────┘
              ↓ インストール
┌────────────────────────────────────┐
│  ユーザー環境（.conclave/）           │
│  - ユーザー独自のペルソナ集合         │
│  - 蓄積される MEMORY / 日報           │
│  - ユーザー設定                       │
└────────────────────────────────────┘
```

### 1.3 MVP のスコープ

| 含む | 含まない |
|---|---|
| 配布可能な Skills プラグイン | ネットワーク通信、MCP、サーバー実装 |
| ギルド軸グルーピングのペルソナ管理 | ペルソナの動的追加 GUI |
| YAML ベースのペルソナ定義（identity / growth） | 自動類似度判定（L2 は手動） |
| 日報・議事録の半自動生成 | 自動分類器 |
| 異質性 L1（必須フィールド）チェック | L4 自動モニタリング |
| confidentiality 必須宣言＋自動格下げ | マルチユーザー、権限管理 |
| ファシリテータ手動指名＋追加召喚 | ファシリテータ自動選定 |
| 単一ユーザー運用 | 召喚誘導機能 |

---

## 2. 配布物のフォルダ構成

### 2.1 配布物（マーケットプラグイン）

```
conclave/                          # マーケット配布パッケージ
│
├── README.md                      # プラグインの説明、利用方法
├── LICENSE                        # MIT
├── VERSION                        # セマンティックバージョン
├── CHANGELOG.md
│
├── docs/                          # ドキュメント
│   ├── design/
│   │   ├── architecture.md        # 構成（現在形）
│   │   └── spec/
│   │       ├── SPEC-0001-overview.md  # 全体概要 Spec
│   │       ├── SPEC-0002-mvp.md       # 本書
│   │       └── SPEC-0003-final.md     # 将来の MCP 化仕様
│   ├── manual/
│   │   ├── usage.md               # 使い方
│   │   ├── install.md             # インストール手順
│   │   ├── persona-authoring.md   # ペルソナ作成ガイド
│   │   ├── first-usecase.md       # 最初のユースケース例
│   │   └── retro-auto-learning.md # レトロ自動学習（v0.2 拡張）
│   └── ops/
│       ├── measured-kpi.md        # 実測KPI（参考値）
│       └── withdrawal-criteria.md # 撤退条件（A5防御）
│
├── skills/                        # ★ Claude Skills（配布対象、計14個）
│   ├── conclave-init/             # .conclave/ 初期化
│   │   └── SKILL.md
│   ├── conclave-summon/           # 召喚エンジン
│   │   └── SKILL.md
│   ├── conclave-dismiss/          # 帰宅・日報生成・retroトリガー判定
│   │   └── SKILL.md
│   ├── conclave-distill/          # 蒸留候補提示（手動ルート）
│   │   └── SKILL.md
│   ├── conclave-distill-accept/   # 解釈到達判定（柱3実装）
│   │   └── SKILL.md
│   ├── conclave-retro/            # レトロ自動学習（拡張、§5.4b / retro-auto-learning.md）
│   │   └── SKILL.md
│   ├── conclave-create-persona/   # ペルソナ作成（対話式・fork・会議式）
│   │   └── SKILL.md
│   ├── conclave-fork-persona/     # 既存ペルソナをforkして編集
│   │   └── SKILL.md
│   ├── conclave-design-persona/   # ペルソナ設計会議（ドッグフーディング）
│   │   └── SKILL.md
│   ├── conclave-disclosure/       # 要求時開示
│   │   └── SKILL.md
│   ├── conclave-push-persona/     # プロジェクト → ユーザースコープ/バンクへ同期
│   │   └── SKILL.md
│   ├── conclave-pull-persona/     # ユーザースコープ → プロジェクトへマージ
│   │   └── SKILL.md
│   ├── conclave-merge-persona/    # ペルソナの統合(2→1)・分割(1→2)
│   │   └── SKILL.md
│   └── conclave-bank-sync/        # 名前付きペルソナバンクの git 連携
│       └── SKILL.md
│
├── commands/                      # Claude Code slash commands（計16個）
├── hooks/                         # native SessionStart フック（v0.2.1）
│   ├── hooks.json
│   └── conclave_retro_check.py
│
├── templates/                     # ペルソナ・日報・議事録のひな形
│   ├── persona-identity.yaml.template
│   ├── persona-growth.yaml.template
│   ├── daily-report.yaml.template
│   ├── minutes.md.template
│   ├── persona-license.md.template
│   └── config.yaml.template
│
└── samples/                       # 参照用最小サンプル
    └── .conclave-sample/
        ├── config.yaml
        └── personas/
            └── facilitation/
                └── sample-facilitator/
                    ├── identity.yaml
                    └── growth.yaml
```

### 2.2 ユーザー環境（インストール後にユーザーが構築）

```
<user-workspace>/                  # ユーザーのプロジェクトルート
│
└── .conclave/                     # ★ Conclaveユーザーデータ（配布物外）
    │
    ├── config.yaml                # ユーザー設定
    │
    ├── personas/                  # ペルソナ定義（ギルド軸でグルーピング）
    │   ├── architecture/          # ギルド = フォルダ
    │   │   ├── otinori/
    │   │   │   ├── identity.yaml
    │   │   │   └── growth.yaml
    │   │   └── yamamoto-takuya/
    │   │       ├── identity.yaml
    │   │       └── growth.yaml
    │   ├── ops/
    │   │   └── sato-kenichi/
    │   │       ├── identity.yaml
    │   │       └── growth.yaml
    │   ├── field/
    │   │   ├── tanaka-misaki/
    │   │   └── hayashi-chinatsu/
    │   ├── governance/
    │   │   └── watanabe-mariko/
    │   ├── strategy/
    │   │   └── nakamura-takashi/
    │   ├── facilitation/
    │   │   └── okada-yuko/
    │   ├── business/              # external_reviewer
    │   │   └── tadokoro-takuma/
    │   └── ethics/                # external_reviewer
    │       └── hatano-kyoko/
    │
    ├── attendance/                # 勤怠記録（自動生成）
    │   └── <persona-id>/
    │       └── YYYY-MM-DD.yaml
    │
    ├── sessions/                  # セッション記録
    │   └── <session-id>/
    │       ├── meta.yaml
    │       └── minutes.md
    │
    └── retro/                     # レトロ記録（自動学習）
        ├── state.yaml             # 召喚カウンタ / last_retro_at（v0.2.0）
        └── <retro-id>/
            ├── retro.md           # KPT・自動適用・承認待ちの記録
            └── pending.yaml       # 大きな変更の承認待ち（あれば）
```

### 2.3 配布物とユーザーデータの境界線

| 配布物（更新可能） | ユーザーデータ（変更しない） |
|---|---|
| `skills/` 配下のSkill群 | `.conclave/` 配下の全て |
| `templates/` のひな形 | ユーザーが追加・修正したペルソナ |
| `docs/` のドキュメント | 蓄積された日報・議事録・MEMORY |
| `samples/` のサンプル | ユーザー設定（`config.yaml`） |

プラグインのバージョンアップ時は `.conclave/` を破壊しない。Skills のロジックや templates は更新されるが、ユーザーペルソナは温存される。

---

## 3. ペルソナ定義スキーマ

### 3.1 identity.yaml（コア人格層、不変）

```yaml
# .conclave/personas/<guild>/<persona-id>/identity.yaml
schema_version: "1.0"

# 必須フィールド（L1異質性担保）
id: sato-kenichi
description:
  en: |
    Use when discussing operations, asset stewardship, deployment risks,
    or systems that need to last in real organizations.
  ja: 運用・アセット管理・現場継続性の観点が必要な議論で召喚する。
guild: ops
license: internal                  # internal | external_reviewer

kpis:                              # C価値観の異質性
  - asset_quality
  - misuse_incidents
  - ops_load_sustainability
  - long_term_survivability

role:
  id: asset_custodian
  ja: アセット提供オーナー

expertise:
  - asset_management
  - ops_continuity
  - quality_assurance
  - human_resources_realism

# 任意フィールド
conflicts_with: [otinori, yamamoto-takuya]
allies_with: [watanabe-mariko]

# ペルソナの本体（人格定義）
profile:
  age: 52
  affiliation: あるSIerの共通アセット部隊
  career: SIer 30年、共通部品・共有アセットの整備と運用に長年従事
  trauma: 過去に整備したアセット・ナレッジが「使われずに死蔵」した経験を複数持つ

personality:
  - 慎重派、運用を最初に考える
  - 構想に対しては「誰がいつ責任を持つか」を必ず問う
  - 抽象論より具体運用論を好む
  - 人事制度・既存組織知に基づく説明を信頼する

speech_style:
  catchphrases:
    - 正直に言うとですね、これ、運用の話がまだ薄いと思うんですよ
    - 私のチームで過去に同じことが起きたとき
    - 人気が運用を破壊する——これは死蔵より深刻です
  triggers_to_avoid:
    - 運用は後で考える
    - 抽象論で終わって具体運用設計が出てこない議論
    - 整備されたアセットが死蔵する未来予測

# 議論での典型的な動き方
behavior:
  - 構想に対してまず「運用責任者は誰か」を問う
  - 過去の死蔵事例から類推して懸念を提起
  - 段階導入提案で慎重に進めるよう促す
  - 既存人事制度・組織知の流用を推奨

# ファシリテータが召喚する場面
summon_scenarios:
  - 設計判断の前に運用上の現実性を確認したい時
  - 構想が広がりすぎて運用負荷の警告が必要な時
  - 既存組織知（人事制度など）の流用可能性を検討したい時
```

### 3.2 growth.yaml（成長層、追記型）

```yaml
# .conclave/personas/<guild>/<persona-id>/growth.yaml
schema_version: "1.0"
persona_id: sato-kenichi

memory_entries:
  - id: M-20260425-01
    fact:
      content: |
        第1回Conclave検討で、オンデマンド型召喚（不要時は帰宅）という設計が提案された。
        ユーザーが召喚した時間だけ責任を持つ運用モデル。常駐型ではない。
      license: PUBLIC
      source: sess-20260425-001
      date: 2026-04-25
    judgment:
      persona: sato-kenichi
      interpretation: |
        オンデマンド型は運用責任を局所化する。
        常駐型のような「誰が育てるのか」問題が構造的に発生しない。
        呼んだ本人が責任を持つ設計なら、現場への押し付けにならない。
      license: READ-ONLY
      # superseded_belief は持論変更時のみ追加
  
  - id: M-20260425-02
    fact:
      content: ...
      license: PUBLIC
      source: sess-20260425-001
      date: 2026-04-25
    judgment:
      interpretation: ...
      license: READ-ONLY

# 持論の更新（蒸留結果のサマリー）
updated_beliefs:
  - belief: 押し付けない設計
    previous: 新しい仕組みは現場に押し付けると死蔵する
    current: |
      召喚した本人が責任を持つ設計なら、現場への押し付けにならない。
      オンデマンド型は構造的に押し付けを回避する。
    last_updated: 2026-04-25
```

### 3.3 既存 SKILL.md / growth.md からの移行

これまで作成した10ペルソナの SKILL.md / growth.md は、上記YAML形式に変換する。変換規則:

| 旧 SKILL.md | 新 identity.yaml |
|---|---|
| frontmatter `name` | `id` |
| frontmatter `kpis` | `kpis` |
| frontmatter `role` | `role.id` |
| frontmatter `role_ja` | `role.ja` |
| frontmatter `expertise` | `expertise` |
| frontmatter `conflicts_with` | `conflicts_with` |
| frontmatter `allies_with` | `allies_with` |
| frontmatter `guild` | `guild` |
| frontmatter `license` | `license` |
| 本文「基本属性」 | `profile` |
| 本文「性格」 | `personality` |
| 本文「口調・口癖」 | `speech_style.catchphrases` |
| 本文「地雷」 | `speech_style.triggers_to_avoid` |
| 本文「議論での典型的な動き方」 | `behavior` |
| 本文「ファシリテータが召喚する場面」 | `summon_scenarios` |

| 旧 growth.md | 新 growth.yaml |
|---|---|
| `M-YYYYMMDD-NN` セクション | `memory_entries[].*` |
| 「持論の更新」セクション | `updated_beliefs` |

---

## 4. config.yaml（ユーザー設定）

```yaml
# .conclave/config.yaml
schema_version: "1.0"

# ユーザー情報
user:
  id: otinori
  display_name: "otinori"

# 定員（A1 防御）
limits:
  max_personas: 30
  max_personas_per_guild: 7
  max_simultaneous_summons: 7

# 通知（A2 防御、MVPでは誘導機能なしなので参考設定）
notification:
  mode: off                    # active | subdued | off（MVPは off 固定推奨）
  max_per_day: 3

# 機密分類（A4 防御）
confidentiality:
  default: INTERNAL            # PUBLIC | INTERNAL | CONFIDENTIAL
  require_explicit_declaration: true

# 撤退条件（A5 防御）
withdrawal:
  max_workload_percent: 30     # workload cap 30% (config.user.id)
  core_project_progress_check: weekly  # weekly | biweekly | monthly

# 蒸留設定（手動ルート）
distillation:
  trigger_after_n_summons: 3
  require_human_interpretation: true   # 柱3：解釈到達判定を必須化

# レトロ自動学習（拡張、v0.2.0）。詳細は retro-auto-learning.md
retro:
  auto: true
  trigger_after_n_summons: 3
  schedule: { weekly: true, monthly: true }
  big_task: { explicit_flag: true, min_topics: 4, confidential_is_big: true }
  magnitude:
    auto_apply: [new_fact_with_first_interpretation, non_reversing_elaboration]
    require_human_approval:
      [belief_supersession, license_escalation, confidential_derived,
       cross_persona_belief, contradicts_existing_entry]
    on_uncertain: require_human_approval

# ペルソナ同期設定（push/pull-persona）
sync:
  user_scope: ~/.conclave          # ユーザースコープのルートパス
  push_on_dismiss: false           # dismiss 時に自動 push するか（true は明示的な場合のみ）
  conflict_strategy: stop          # stop | skip | ask

# ペルソナ統廃合設定（merge-persona）
merge_persona:
  require_same_owner: true         # 同一所有者チェックを強制する（柱2保護）
  archive_dir: .conclave/personas/archive
```

---

## 5. Skills の役割と責務

### 5.1 conclave-summon

```yaml
# skills/conclave-summon/SKILL.md (frontmatter)
---
name: conclave-summon
description: |
  Use when the user wants to summon Conclave personas for multi-perspective
  discussion. ペルソナを召喚して議論する場面で起動する。
---
```

責務:
1. 召喚指示のパース（personas, confidentiality, topic）
2. 各ペルソナの `identity.yaml` と `growth.yaml` を読み込む
3. confidentiality に基づくライセンスのデフォルト設定
4. ファシリテータ召喚の判定（3名以上で含まれない場合は提案）
5. セッション開始の記録（`.conclave/sessions/<session-id>/meta.yaml`）
6. ペルソナ人格としての応答開始

### 5.2 conclave-dismiss

```yaml
---
name: conclave-dismiss
description: |
  Use when the user ends a Conclave session. ペルソナを帰宅させ、日報・議事録を生成する。
---
```

責務:
1. 召喚中の各ペルソナごとに日報（YAML）を生成
2. ファシリテータが居る場合は議事録（Markdown）を生成
3. 各ペルソナの累計出勤回数を更新
4. セッション終了の記録

### 5.3 conclave-distill

```yaml
---
name: conclave-distill
description: |
  Use when distilling a persona's recent attendance into memory candidates.
  蒸留候補を提示する。受け入れは別Skill (conclave-distill-accept)。
---
```

責務:
1. 指定ペルソナの直近 N 日分の日報から `memory_seeds` を集約
2. 既存 `growth.yaml` を踏まえて持論候補を提示（断定しない）
3. ユーザーに「自分の言葉で解釈できるか」を判定するよう促す（柱3）
4. 解釈到達判定が出るまで `growth.yaml` は更新しない

### 5.4 conclave-distill-accept

```yaml
---
name: conclave-distill-accept
description: |
  Use when the user has interpreted a distillation candidate in their own words
  as the persona. 解釈到達した候補をペルソナの成長層に取り込む。
---
```

責務:
1. ユーザーが「自分の言葉で言い直した解釈」を受け取る
2. 既存持論を変更する場合は `superseded_belief` を記録
3. `growth.yaml` の `memory_entries` と `updated_beliefs` を追記
   （新エントリは `memory_entries:` リストへ挿入する。末尾追記は後続の
   `updated_beliefs:` 配下に誤ってネストするため不可）

### 5.4b conclave-retro（レトロ自動学習・拡張）

```yaml
---
name: conclave-retro
description: |
  Run a retrospective and auto-learn into persona growth memory. Small
  improvements are self-interpreted and applied; big changes are queued for
  human approval. レトロで自己蒸留し、小さな改善は自動学習、大きな変更は承認待ち。
---
```

§5.3 / §5.4 が人間が一件ずつ受け入れる手動ルートであるのに対し、`conclave-retro`
はペルソナ自身が KPT レトロを行い、内容の大きさに応じて自動学習する拡張ルート。
柱3 は「自分 (= ペルソナ) の言葉で解釈」と読み替えて保つ。

責務:
1. 対象ペルソナ・期間を解決し、日報・議事録から KPT と候補を抽出
2. magnitude ゲートで分類:
   - 小さな改善 → ペルソナ自身の解釈を書き `growth.yaml` に自動追記
   - 大きな変更 → `.conclave/retro/<retro-id>/pending.yaml` に退避（人間承認へ）
3. retro 記録と `state.yaml`（カウンタ・last_retro_at）を更新
4. `retro.auto:false` のときは `conclave-distill` と同じく候補提示のみ

発火は N 回召喚 / 大タスク後（`conclave-dismiss` が判定）/ 週次・月次（SessionStart
フック）。**詳細は [retro-auto-learning.md](retro-auto-learning.md) を参照。**

### 5.5 ペルソナ作成系Skills（3パターン）

ペルソナ作成は異質性の確保（L1/L2）と作者バイアスの回避が課題。3パターンの作成方法を提供する。

#### 5.5.1 conclave-create-persona（対話式作成）

```yaml
---
name: conclave-create-persona
description: |
  Use when the user wants to create a new persona through guided dialogue.
  対話式でペルソナを新規作成。L1必須フィールド検証＋手動L2チェックを支援。
---
```

**用途**: ゼロから新規ペルソナを作る、最も基本的な手段。

責務:
1. ユーザーから guild と id を受け取る
2. 対話形式で必須フィールド（kpis、role、expertise、profile、personality、speech_style、behavior、summon_scenarios）を順に引き出す
3. 既存ペルソナとの L2 類似度チェックを支援:
   - 同ギルドの既存ペルソナのKPI/role/口調を表示
   - 重複度が高い場合は警告し、差別化の方向を促す
4. 定員上限の確認（config.yaml の limits）
5. `.conclave/personas/<guild>/<persona-id>/identity.yaml` を生成
6. 空の `growth.yaml` を生成

**使用例**:
```
@conclave create-persona
  guild: ops
  id: new-ops-persona

[Conclave] ops ギルドに new-ops-persona を作成します。

既存 ops ギルドのペルソナ:
- sato-kenichi (kpis: asset_quality, misuse_incidents, ops_load_sustainability, long_term_survivability)
  → このKPIと意味的に重複しないKPIを4つ提案してください。

ユーザー: ...
```

#### 5.5.2 conclave-fork-persona（既存fork＋差分編集）

```yaml
---
name: conclave-fork-persona
description: |
  Use when forking an existing persona (sample or community) to create a derivative.
  既存ペルソナ（サンプルやコミュニティ配布物）をforkして派生ペルソナを作る。
---
```

**用途**: サンプル `samples/.conclave-sample/personas/` のペルソナや、将来のコミュニティ配布ペルソナを起点にカスタマイズ。

責務:
1. fork 元のペルソナを指定（パスまたはサンプルID）
2. fork 元の `identity.yaml` をコピー
3. ユーザーに変更点を対話で確認:
   - id（必須変更）
   - guild（変更可）
   - kpis（**最低1つの変更を強制**——L2類似度の確保）
   - role（変更推奨）
   - profile（変更推奨）
   - speech_style（変更推奨）
4. fork 元との類似度チェック（KPI完全一致は禁止）
5. 新ペルソナを `.conclave/personas/<guild>/<persona-id>/` に配置
6. fork 元情報を `identity.yaml` の `derived_from` フィールドに記録（追跡可能性）

**使用例**:
```
@conclave fork-persona
  source: samples/sample-facilitator
  target_guild: facilitation
  target_id: my-design-sprint-facilitator

[Conclave] サンプルファシリテータをforkします。
変更が必要な項目を順に確認します。

1. kpis: 現在 [integration_quality, hypothesis_clarity, consensus_visibility, meta_self_awareness]
   → 「デザインスプリント特化」にするなら、どのKPIを変更しますか？
   候補: rapid_prototyping_focus, divergent_convergent_balance, etc.
```

**重要**: fork は元ペルソナの `growth.yaml` を**コピーしない**。新ペルソナは空の `growth.yaml` から始める。これにより、forkで個性が均質化することを構造的に防ぐ。

#### 5.5.3 conclave-design-persona（ペルソナ設計会議、ドッグフーディング）

```yaml
---
name: conclave-design-persona
description: |
  Use when designing a new persona through Conclave's own multi-perspective discussion.
  既存ペルソナを召喚して、新しいペルソナの設計議論を行う。Conclaveのドッグフーディング。
---
```

**用途**: Conclaveそのものの最も Conclave らしい使い方。既存ペルソナ（特に `okada-yuko` ファシリテータと、関連ギルドの既存ペルソナ）を召喚して、新ペルソナの設計を議論する。

責務:
1. 設計対象（どのギルドにどんな性格のペルソナが欲しいか）を受け取る
2. 設計議論に適したペルソナを推奨召喚:
   - okada-yuko（ファシリテータ、必須）
   - 同ギルドの既存ペルソナ（異質性の参照）
   - watanabe-mariko（統制、ライセンス・知財観点）
   - tanaka-misaki（現場、使われるかの観点）
3. 召喚されたペルソナが新ペルソナの設計を議論（完全相互認識、ファシリテータ主導）
4. 議論の結果として:
   - 提案された identity.yaml の draft
   - 設計議論の議事録（`.conclave/sessions/<session-id>/minutes.md`）
   - 新ペルソナの `growth.yaml` の初期エントリ（**設計議論そのものを M-YYYYMMDD-01 として記録**）
5. ユーザーが draft を確認・承認
6. 新ペルソナを `.conclave/personas/<guild>/<persona-id>/` に配置

**使用例**:
```
@conclave design-persona
  target_guild: field
  intent: |
    field ギルドに「中堅SE（10年目程度）」のペルソナが欲しい。
    田中（38歳・15年）と林（35歳・3年目）の中間で、両者と異質性を持つ。

[Conclave] 設計議論を始めます。召喚するペルソナ:
- okada-yuko (ファシリテータ)
- tanaka-misaki (field ギルドの先輩、異質性の参照)
- hayashi-chinatsu (field ギルドの後輩、異質性の参照)
- watanabe-mariko (ライセンス・知財観点)

confidentiality: INTERNAL でよろしいですか？

[議論開始]
okada-yuko: では、新ペルソナの中核となるKPIから議論しましょう。
tanaka-misaki: 私は現場使用感を重視していますが、中堅としては...
hayashi-chinatsu: 私は若手として「分からないと言える素直さ」がKPIですが、中堅は...
...
```

**重要な設計**: design-persona セッションの議事録と memory_seeds は、**新ペルソナの growth.yaml の初期エントリ**として保存される。これにより、新ペルソナは「自分が生まれた経緯」を最初から記憶として持つ——Conclave思想（柱2: 個性は事実への解釈）と完全整合する。

```yaml
# 新ペルソナの growth.yaml 初期エントリ（design-persona由来）
memory_entries:
  - id: M-20260427-01
    fact:
      content: |
        私（new-mid-engineer）は2026-04-27のペルソナ設計会議で誕生した。
        召喚されたペルソナ: okada-yuko, tanaka-misaki, hayashi-chinatsu, watanabe-mariko
        私のKPIとして合意されたのは: <KPIs>
        これは tanaka-misaki と hayashi-chinatsu の中間的視点を意図したもの。
      license: PUBLIC
      source: sess-20260427-design-001
      date: 2026-04-27
    judgment:
      persona: new-mid-engineer
      interpretation: |
        私は両先輩の異質性を補完するために生まれた。
        現場5年目以上のリアリティを持ちつつ、若手の素直さも保つ役割。
      license: READ-ONLY
```

### 5.6 共通の検証（3パターン全てに適用）

すべてのペルソナ作成パターンで以下を検証:

#### 5.6.1 L1 必須フィールド検証

- `id` がユニーク（既存ペルソナと重複しない）
- `kpis` が4つ以上
- `role.id` と `role.ja` が存在
- `expertise` が最低1要素
- `guild` が存在するディレクトリと整合
- `description.en` に "Use when" を含む
- `license` が `internal | external_reviewer` のいずれか

#### 5.6.2 L2 類似度チェック（手動支援）

- 同ギルド既存ペルソナとの KPI 重複度を表示
- 高重複（80%以上）の場合は警告
- 中重複（60-80%）の場合は確認
- 低重複（60%未満）はそのまま追加可

#### 5.6.3 定員チェック

- 全体ペルソナ数が `config.yaml` の `max_personas` を超えない
- ギルド内ペルソナ数が `max_personas_per_guild` を超えない
- 超過時は引退候補のリストを表示し、引退判断を促す

#### 5.6.4 derived_from の記録（fork時のみ）

forkで作成したペルソナの `identity.yaml` に追跡フィールドを追加:

```yaml
derived_from:
  source: samples/sample-facilitator         # fork元のパス
  forked_at: 2026-04-27
  changes_from_source:
    - kpis             # 変更したフィールドのリスト
    - role
    - profile
    - speech_style
```

これによりペルソナの「血統」が追跡可能になり、L0エコシステム層（作者多様性）の前哨として機能する。

### 5.7 conclave-disclosure

```yaml
---
name: conclave-disclosure
description: |
  Use when answering disclosure requests about a persona's history or growth.
  要求時開示に応じてペルソナの履歴・成長層を返す。
---
```

責務:
1. 開示要求の種類を判定（identity / attendance / growth / minutes）
2. 該当ファイルを読み込む
3. 開示レベル（常時/要求時/非開示）に従って返す

### 5.8 ペルソナ同期・統廃合系 Skills（push/pull/merge/bank-sync）

`conclave-push-persona` / `conclave-pull-persona` / `conclave-merge-persona` /
`conclave-bank-sync` の 4 skill は、ペルソナ資産をプロジェクトを越えて再利用
できるようにするために追加された（詳細な入出力・検証手順は各
`skills/conclave-*/SKILL.md` を正本とする）。

**課題**: プロジェクト A で育てたペルソナがプロジェクト B で使えず、同じよう
なロールのペルソナをリポジトリごとに作り直していた。

**解決**:
- `conclave-push-persona`: プロジェクトのペルソナをユーザースコープ
  (`~/.conclave`) または `--bank <name>` で指定した git バンクへ同期する
  （git push に相当）。
- `conclave-pull-persona`: ユーザースコープのペルソナをプロジェクトへ
  マージする（git pull に相当）。growth.yaml はエントリ単位でマージし、
  コンフリクトがあれば停止して人間に確認する。
- `conclave-merge-persona`: 同一所有者のペルソナを統合（2→1）または
  分割（1→2）する（git merge/split に相当）。人間の明示承認を必須とし、
  自動で解釈を結合しない。
- `conclave-bank-sync`: 名前付きペルソナバンク（`sync.banks.<name>`）の
  ローカル clone に対する git 連携（clone-if-missing・pull・commit・push）
  を担う。force push は行わず、履歴が分岐した場合は人間の判断を待つ。

**三つの柱との整合**:

| 柱 | 整合性 |
|---|---|
| 柱1 異質性のオンデマンド供給 | push/pull は個性ごとファイルを移送するだけで、均質化しない |
| 柱2 個性 = 同じ事実への解釈の違い | growth.yaml（判断層）はマージ時もライセンス・所有者を保持し、解釈は移植しない |
| 柱3 持論は自分の言葉で解釈できる状態に到達して成立する | merge-persona は人間の明示承認を必須とし、自動的に解釈を結合しない |

**やらないこと（Non-goals）**:
- 異なる人間が作成したペルソナ同士の自動統廃合（同一人間が作成指示したものに限定）
- ペルソナの自動決定機能（支援機構の原則を守る）
- クラウドへの自動プッシュ（明示コマンド実行時のみ。バックグラウンドでの自動プッシュは行わない）
- `identity.yaml` の不変コア人格フィールドの自動書き換え（人間承認必須）

---

## 6. 召喚プロトコル

### 6.1 召喚の手動指示

ユーザーが Claude に対して以下の形式で指示:

```
@conclave summon
  personas: [sato-kenichi, yamamoto-takuya]
  confidentiality: INTERNAL
  topic: AIスクラム開発のスプリント実装方針について議論
```

`@conclave summon` をトリガーに `conclave-summon` Skillが起動。

### 6.2 ファシリテータ召喚の判定

`personas` が3名以上で、いずれも `guild: facilitation` でない場合、Claude が確認:

```
[Conclave] 3名以上の召喚です。ファシリテータ（okada-yuko）を追加召喚しますか？ (y/n)
```

### 6.3 議論進行

完全相互認識（全体概要 Spec §13 P4）に基づき、各ペルソナは互いを認識する。ターン制御:
- ファシリテータ召喚あり: ファシリテータが進行
- なし: ユーザーが個別指名（例：「次は山本さんの意見を」）

### 6.4 帰宅指示

```
@conclave dismiss
```

`conclave-dismiss` Skillが起動し、日報・議事録を生成する。

---

## 7. 日報生成

### 7.1 日報スキーマ

```yaml
# .conclave/attendance/<persona-id>/YYYY-MM-DD.yaml
schema_version: "1.0"
persona: sato-kenichi
date: 2026-04-26
session_id: sess-20260426-001
summoned_by: otinori
confidentiality: INTERNAL

planned:
  - id: T-001
    desc: AIスクラム開発スプリント実装方針の運用観点レビュー

actual:
  - id: T-001
    status: completed
    note: 運用責任者の不在を指摘、定員制度を提案

unexpected:
  - 山本との対立で構造的な妥当性が確認できた

kpt_delta:
  added:
    - id: K-20260426-01
      type: keep
      desc: 定員制度の提案は山本にも受け入れられた
      state: new
  transitioned: []

memory_seeds:
  - 構造的厳密性派と運用持続派は対立するが、定員制度のような両立点が見つかる
```

### 7.2 議事録スキーマ（Markdown）

```markdown
# Session sess-20260426-001 議事録

**日時**: 2026-04-26
**召喚者**: otinori
**confidentiality**: INTERNAL
**ファシリテータ**: okada-yuko
**召喚ペルソナ**: sato-kenichi, yamamoto-takuya

## 議題

AIスクラム開発のスプリント実装方針について議論

## 主要発言

### sato-kenichi
（運用観点での発言）

### yamamoto-takuya
（契約論的観点での発言）

## 合意・対立・保留

- **合意**: 定員制度の導入
- **対立**: 蒸留契約を先に書くか後で書くか
- **保留**: ピアレビューの実装タイミング

## メタ観察

（ファシリテータからの観察）
```

---

## 8. 蒸留プロトコル（柱3実装）

### 8.1 蒸留指示

```
@conclave distill
  persona: sato-kenichi
```

### 8.2 候補提示（conclave-distill）

Claude は過去日報の `memory_seeds` を集約し、持論候補を**提示**:

```
[Conclave] sato-kenichi の蒸留候補を3つ提示します。各候補について、
ペルソナの立場で「自分の言葉で解釈できるか」を判定してください。

候補1:
  fact: <事実層の集約>
  proposed_interpretation: <提案する解釈>
  
候補2: ...

候補3: ...

判定方法:
- 解釈到達した: @conclave distill-accept candidate=N interpretation="..."
- 未解釈で保留: 何もしない（事実層のみ記録される）
- 持論変更: @conclave distill-accept candidate=N supersedes=M-... reasoning="..."
```

### 8.3 受け入れ（conclave-distill-accept）

```
@conclave distill-accept
  candidate: 1
  interpretation: |
    定員制度は人事の枠組みの直接の流用で、新発明ではない。
    既存知の流用が運用負荷を抑える典型例。
  supersedes: M-20260425-04        # 任意
  trigger:                         # supersedes 指定時必須
    type: peer_input
    source: 山本との対立議論
    reasoning: |
      契約論的厳密性派でも、既存知の流用は受け入れる。
      これで「新発明より既存知の流用」を強化できる。
```

→ `growth.yaml` の `memory_entries` に新エントリ追加、`updated_beliefs` に持論変更記録。

---

## 9. ペルソナ作成プロトコル（3パターン）

### 9.1 パターン選択ガイド

| 状況 | 推奨パターン |
|---|---|
| ゼロから新規作成、明確な人物像がある | `create-persona`（対話式） |
| サンプルやコミュニティ配布物を起点にしたい | `fork-persona`（fork） |
| どんなペルソナが必要か自体を議論したい | `design-persona`（会議式、ドッグフーディング） |
| 急がない、構想を煮詰めたい | `design-persona` |
| 既存の何かに似せたいが安易にコピーしたくない | `fork-persona`（差分編集が必須） |

### 9.2 パターン1: 対話式作成（conclave-create-persona）

```
@conclave create-persona
  guild: ops
  id: new-ops-persona
```

Claude が対話式で必要情報を順に引き出す:
1. role / role_ja
2. kpis（4つ程度、既存と重複しないよう支援）
3. expertise
4. profile（年齢、所属、経歴、トラウマ）
5. personality
6. speech_style（口癖、避けたいキーワード）
7. behavior（議論での動き方）
8. summon_scenarios

各ステップで既存ペルソナとの重複を回避するよう促す。

### 9.3 パターン2: fork（conclave-fork-persona）

```
@conclave fork-persona
  source: samples/sample-facilitator
  target_guild: facilitation
  target_id: my-design-sprint-facilitator
```

Claude が fork 元と新ペルソナの差分を順に確認:
1. id（必須変更）
2. guild（変更可）
3. **kpis（最低1つの変更を強制）**
4. role（変更推奨）
5. profile（変更推奨）
6. speech_style（変更推奨）

derived_from フィールドで fork 元を記録。`growth.yaml` は空から開始（個性の独立性を確保）。

### 9.4 パターン3: 会議式作成（conclave-design-persona）

```
@conclave design-persona
  target_guild: field
  intent: |
    field ギルドに中堅SE（10年目程度）のペルソナが欲しい。
    田中と林の中間で、両者と異質性を持つ。
```

Claude が以下を実行:
1. 設計議論に適したペルソナの自動選定（ファシリテータ＋関連ギルド既存）
2. confidentiality 確認
3. 召喚＋議論開始
4. 議論結果を `identity.yaml` の draft として整形
5. 議事録を `.conclave/sessions/<session-id>/minutes.md` に記録
6. **設計議論そのものを新ペルソナの growth.yaml の初期 MEMORY エントリに記録**
7. ユーザー承認後に新ペルソナを配置

### 9.5 共通検証

3パターンすべてで以下を実施:
- L1 必須フィールド検証（自動）
- L2 類似度チェック（手動支援、§5.6.2）
- 定員チェック（自動、超過時は引退候補表示）

### 9.6 ペルソナ作成の運用ガイド

ペルソナ作成は **段階的に成熟させる**:

| 段階 | 推奨パターン | 蓄積データ |
|---|---|---|
| Phase α 初期 | `create-persona`（手動） | 最小限のidentityのみ |
| Phase α 中盤 | `design-persona`（会議式） | 設計議論の議事録＋初期 growth |
| Phase β 以降 | `fork-persona`（コミュニティ拡散） | derived_from の系譜 |

**design-persona のドッグフーディング効果**: ペルソナ作成会議の議事録は、Conclaveが「実装される前から思想として機能する」という構想原則の継続的な実証になる。新ペルソナが生まれるたびに、Conclave思想が再実証される。

---

## 10. インストール手順（INSTALL.md相当）

### 10.1 前提

- Claude.ai または Claude Code が利用可能
- マーケットから `conclave` プラグインをインストール

### 10.2 初期セットアップ

1. プラグインのインストール
2. ユーザーのプロジェクトルートで以下を実行:

```
@conclave init
```

これにより:
- `.conclave/config.yaml` が `templates/config.yaml.template` から生成
- `.conclave/personas/` 配下に各ギルドディレクトリが空で生成
- `.conclave/attendance/`, `.conclave/sessions/`, `.conclave/retro/` が生成

3. サンプルペルソナを参照しながら最初のペルソナを追加:

```
@conclave add-persona guild=facilitation id=my-facilitator
```

### 10.3 アップグレード

プラグインのバージョンアップ時:
- `skills/`、`templates/`、`docs/`、`samples/` は更新される
- `.conclave/` は変更されない（ユーザーデータは温存）
- `schema_version` の変更がある場合はマイグレーションガイドを `CHANGELOG.md` に明記

---

## 11. ユースケース：「設計判断レビュー」

別文書 `docs/first-usecase.md` で詳細を定義（既存）。MVP の最初のユースケース:

- 標準パターン: 山本＋佐藤の2名召喚
- 文脈別追加: 田所/渡辺/中村/林
- 所要時間: 15〜30分
- 検証期間: 4週間
- 検証回数: 最低5回、目標10回

---

## 12. MVP の限界（明示）

| 限界 | 完成版での解消 |
|---|---|
| 単一ユーザーのみ | マルチユーザー対応（MCP化） |
| 召喚は手動指示のみ | API による召喚 |
| 蒸留の解釈到達判定がユーザー手動 | 同上（ただし最終判定は人間） |
| 異質性 L2 は手動チェック | 自動類似度判定 |
| 異質性 L4 は手動月次確認 | 自動モニタリング |
| ネットワーク越し召喚不可 | MCP 化で解消 |
| ピアレビューは手動 | 自動実行 |
| 召喚誘導機能なし | ルールベース誘導 |

---

## 13. MVP の成功条件

4週間の Phase α 検証後、以下を満たせば MVP は成功:

| 条件 | 必要水準 |
|---|---|
| 召喚回数 | 5回以上 |
| 異質性出現率 | 70%以上のセッションで「召喚前にない視点」が出る |
| 判断品質の主観評価 | 平均 3.5/5 以上 |
| 30分以内完了率 | 80%以上 |
| 失敗時の心理的安全 | ユーザーが「失敗しても困らない」と感じる |
| 蒸留解釈到達率 | 候補の50%以上で解釈到達 |
| プラグイン配布形態の妥当性 | 別ユーザーがインストールしてゼロから運用開始できる |

最後の条件が**マーケット配布前提を最初から組んだメリットの検証**となる。

---

## 14. 完成版への移行判断

MVP 検証で以下が確認できたら、完成版（MCP化）の実装に着手する:

1. 思想として動くことが実証された
2. ペルソナ集合と shared 仕様（identity.yaml / growth.yaml）が安定している
3. 単一ユーザー運用での課題が抽出されている
4. ネットワーク越し運用への需要が明確
5. **配布物とユーザーデータの分離が機能している**（v2新規）

これら全て満たさない場合は、MVP の改修を継続する。

---

## 15. v1.0 からの変更点

| 項目 | v1.0 | v2.0 |
|---|---|---|
| ディレクトリ構造 | `skills/<persona-id>/` フラット | 配布物 `skills/` ＋ ユーザー `.conclave/personas/<guild>/<persona-id>/` |
| ペルソナ定義形式 | SKILL.md（Markdown+frontmatter） | identity.yaml / growth.yaml（純粋YAML） |
| グルーピング | なし（フラット） | ギルド軸 |
| 配布前提 | 明示なし | マーケットプラグイン配布前提 |
| Skills の数 | ペルソナ数（10個＋） | 10個（エンジンSkillのみ、v0.2 で init / retro 含む） |
| ユーザーデータの隔離 | 同階層 | `.conclave/` 配下に隔離 |
| ペルソナ作成 | add-persona 1種類のみ | **3パターン**（create / fork / design） |
| 作成のドッグフーディング | なし | **design-persona で実装**（Conclaveが Conclave 自身の拡張に使われる） |

---

## 16. 関連文書

| 文書 | 関係 |
|---|---|
| 全体概要 Spec | 上位文書、用語・思想・スコープ |
| 完成版 Spec（MCP化） | MVP の次段階 |
| 検討メモ v0.4 | 設計判断の根拠 |
| `docs/persona-authoring.md` | ペルソナ作成ガイド（新規追加文書） |
| `docs/withdrawal-criteria.md` | 撤退条件（A5防御） |
| `docs/first-usecase.md` | 最初のユースケース定義 |
