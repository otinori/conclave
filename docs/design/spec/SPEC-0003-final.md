# Conclave 完成版 Spec — MCP化（ネットワーク越し）

**版**: 1.0
**作成日**: 2026-04-26
**対象**: Phase β（クローズド）／Phase γ（OSS的オープン公開）
**実装基盤**: MCP（Model Context Protocol）サーバー＋クライアント
**前提**: 全体概要 Spec ／ MVP Spec を読了済み、Phase α 検証完了

---

## 1. 完成版の目的とスコープ

### 1.1 目的

MVP で動いた Conclave 思想を、**ネットワーク越しに複数ユーザー・複数組織**で実行可能にする。AIペルソナをサーバー側で管理し、ユーザーは MCP 経由で召喚・対話する。

### 1.2 完成版のスコープ

| 含む | 含まない（MVPと同様） |
|---|---|
| MCP サーバー実装（Conclave Engine） | 最終決定責任の自動化 |
| MCP クライアント API（召喚・帰宅・蒸留） | ペルソナ依存症の上流対策 |
| マルチユーザー、権限管理 | モデル中立性の自動保証 |
| 異質性 L2 自動類似度判定 | 集合的記憶の中央集権実装（Memory MCP委譲） |
| 異質性 L4 運用中モニタリング | 法的判断・統制（既存組織機構へ） |
| 召喚誘導機能（ルールベース） | — |
| ピアレビュー機能 | — |
| ギルド内 MEMORY 共有の自動化 | — |
| 議事録・日報の半自動生成 | — |
| 説明可能性の3層（要求時開示API含む） | — |

### 1.3 動作環境

| 項目 | 内容 |
|---|---|
| サーバー | MCPサーバー（Streamable HTTP / SSE） |
| ストレージ | SQLite（Phase β）→ PostgreSQL（Phase γ） |
| クライアント | Claude Code、Claude.ai、その他MCP対応AIクライアント |
| 認証 | OAuth2 / API Key（Phase β は API Key、Phase γ は OAuth） |
| ユーザー | マルチユーザー、組織単位の権限管理 |

---

## 2. アーキテクチャ

### 2.1 全体図

```
┌──────────────────────────────────────────────────────┐
│  AI Client（Claude Code / Claude.ai / その他MCP対応AI）│
└──────────────────────┬───────────────────────────────┘
                       │ MCP (Streamable HTTP / SSE)
                       │
        ┌──────────────▼──────────────┐
        │   Conclave MCP Server       │
        │   (Conclave Engine)         │
        └──┬────────┬────────┬────────┘
           │        │        │
   ┌───────▼──┐ ┌──▼──────┐ ┌▼──────────┐
   │ Persona  │ │ Session │ │ Memory    │
   │ Registry │ │ Manager │ │ Distiller │
   └──────────┘ └─────────┘ └───────────┘
           │        │        │
        ┌──▼────────▼────────▼──┐
        │  Storage Layer        │
        │  (SQLite/PostgreSQL)  │
        └───────────────────────┘
```

### 2.2 主要コンポーネント

| コンポーネント | 役割 |
|---|---|
| **Conclave Engine** | MCP リクエストの受信・ルーティング |
| **Persona Registry** | SKILL.md / growth.md の管理、L1/L2チェック |
| **Session Manager** | 召喚・帰宅・対話セッション管理、勤怠記録 |
| **Memory Distiller** | 蒸留Skill の実行、解釈到達判定の支援 |
| **Storage Layer** | ペルソナ定義、MEMORY、勤怠、議事録、日報の永続化 |

### 2.3 3層スコープ分離の実装

| 層 | 実装 | 公開範囲 |
|---|---|---|
| **エンジン層** | Conclave MCP Server のコード | OSS（Apache-2.0 等、Phase γ） |
| **ペルソナ定義層** | 各組織独自の SKILL.md / growth.md | 組織独自、外部公開しない |
| **MEMORY層** | growth.md 内の各エントリ、ライセンス単位制御 | エントリ単位 |

---

## 3. MCP API 仕様

### 3.1 提供ツール一覧

| ツール名 | 機能 |
|---|---|
| `conclave_summon` | ペルソナ召喚 |
| `conclave_dismiss` | 帰宅指示 |
| `conclave_speak` | 召喚中ペルソナの発言取得 |
| `conclave_distill` | 蒸留実行（候補提示、手動ルート） |
| `conclave_retro` | レトロ自動学習（小=自己解釈で自動適用、大=承認待ち。`retro-auto-learning.md`） |
| `conclave_list_personas` | 利用可能ペルソナ一覧 |
| `conclave_open_disclosure` | 要求時開示（成長層・日報等） |
| `conclave_attendance` | 勤怠情報取得 |

MVP の `recommend` / `search` / `conflict_check` は提供しない（Skill選定能力に委ねる原則を踏襲）。

### 3.2 conclave_summon

```yaml
input:
  personas: [persona-id, ...]    # 必須、最低1名
  confidentiality: PUBLIC | INTERNAL | CONFIDENTIAL  # 必須
  topic: <議題、5行以内>          # 任意
  facilitator: persona-id         # 任意、3名以上召喚時に推奨
  
output:
  session_id: <uuid>
  summoned_personas:
    - id: persona-id
      core_identity: <SKILL.md の主要属性>
      growth_summary: <最新の持論サマリー、READ-ONLY層は除外>
  facilitator_proposal: <自動提案、3名以上で含まれない場合>
```

**事前条件**:
- 全 personas が Persona Registry に登録済み
- 同一 persona-id の未帰宅セッションが存在しない
- 召喚者が該当ペルソナへのアクセス権を持つ

**事後条件**:
- セッションが Session Manager に登録される
- 各ペルソナの出勤回数 +1
- L3 召喚時の KPI 重複警告が出力される（推奨実装）

### 3.3 conclave_dismiss

```yaml
input:
  session_id: <uuid>              # 必須
  generate_minutes: bool          # 任意、3名以上召喚時はtrueデフォルト
  
output:
  daily_reports:
    - persona: persona-id
      yaml_path: <attendance/.../YYYY-MM-DD.yaml>
  minutes_path: <sessions/.../minutes.md>  # generate_minutes=true時
  duration_minutes: <int>
```

**事後条件**:
- 各召喚されたペルソナの日報が生成される
- 議事録が指定された場合は生成される
- セッションが Session Manager から削除される
- 累計勤怠が更新される

### 3.4 conclave_speak

```yaml
input:
  session_id: <uuid>
  persona: persona-id
  prompt: <発言を促すプロンプト>
  
output:
  utterance: <ペルソナの発言>
  meta:
    referenced_growth_entries: [M-..., ...]
    interpretation_state: solid | interpreting | unclear
```

`interpretation_state` は柱3に基づく:
- `solid`: 該当持論が解釈済み（自分の言葉で言える）
- `interpreting`: 解釈途中（事実は知っているが、自分の言葉になっていない）
- `unclear`: 未解釈

### 3.5 conclave_distill

```yaml
input:
  persona: persona-id              # 必須
  trigger: scheduled | manual | conflict_detected
  candidates_only: bool            # デフォルトtrue（柱3：候補提示のみ）
  
output:
  candidates:
    - candidate_id: <uuid>
      fact_layer:
        content: <事実>
        license: <自動格下げ後>
      proposed_judgment:
        interpretation: <提案する解釈>
        confidence: low | medium | high
        sources: [<日報のmemory_seeds参照>]
      requires_human_judgment: true
      
  pending_review_count: <int>
```

ユーザー（または委譲された別Skill）が、各候補について「自分の言葉で解釈できるか」を判定し、`accept` または `reject` する。

### 3.6 conclave_distill_accept

```yaml
input:
  candidate_id: <uuid>
  user_interpretation: <ユーザーがペルソナとして言い直した解釈>
  supersedes: M-YYYYMMDD-NN        # 任意、持論変更時のみ
  trigger:                          # supersedes 指定時は必須
    type: fact_evidence | peer_input | external_review | other
    source: <変更のきっかけ>
    reasoning: <自分の言葉での変更理由>
  
output:
  memory_entry_id: M-YYYYMMDD-NN
  growth_md_updated: true
```

### 3.6b conclave_retro（レトロ自動学習・拡張）

`conclave_distill` / `conclave_distill_accept` が手動ルートなのに対し、ペルソナ自身が
レトロを行い、内容の大きさで自動適用と人間承認を振り分ける。柱3 は「自分=ペルソナの
解釈」で保つ。詳細は `retro-auto-learning.md`。

```yaml
input:
  personas: [<persona-id>, ...]     # 任意。既定は最後の retro 以降に活動した全員
  scope: { since: <date> } | { last_n_sessions: <int> }   # 任意
  trigger: n_summons | big_task | schedule | manual
  dry_run: false                    # true なら distill 相当（提示のみ）

output:
  auto_applied: [M-YYYYMMDD-NN, ...]   # 小さな改善（自己解釈で適用済み）
  pending: [<candidate>, ...]          # 大きな変更（人間承認待ち）
  retro_id: <retro-id>
```

### 3.7 conclave_open_disclosure

説明可能性の3層に基づく要求時開示API:

```yaml
input:
  request_type: persona_summary | recent_attendance | growth_layer | session_minutes
  target: persona-id | session-id
  scope: brief | detailed | specific_event
  
output:
  data: <要求された情報>
  redacted_fields: [<開示制限により省略された項目>]
```

非開示項目（他組織から取り込んだペルソナ内部、他ユーザーの召喚履歴等）は redacted_fields に明示される。

---

## 4. 異質性担保の自動化

### 4.1 L1 定義時チェック（必須、自動）

ペルソナ追加 API で以下を自動検証:

```yaml
input:
  skill_md_content: <SKILL.md フロントマター＋本文>
  
validation:
  - kpis フィールドが必須かつ非空
  - role / role_ja が必須
  - expertise が最低1要素
  - guild が登録済みギルドのいずれか
  - description に "Use when" を含む
  
output:
  ok: bool
  errors: [<検証エラー>]
```

### 4.2 L2 作成時チェック（必須、自動）

新規ペルソナ追加時に既存ペルソナと自動類似度判定:

```yaml
similarity_check:
  - kpis 重複度: 既存ペルソナの kpis との意味的類似度（embedding ベース）
  - role 重複度: 既存 role / role_ja との類似度
  - 文体類似度: 経歴・口調セクションの類似度
  
thresholds:
  high: > 0.85    # 人間レビュー必須、自動弾かない
  medium: 0.6-0.85  # 警告表示、追加可能
  low: < 0.6      # そのまま追加
```

### 4.3 L3 召喚時チェック（推奨、自動）

`conclave_summon` 内で召喚予定者間の KPI 重複度を計算:

```yaml
session_diversity_score:
  kpi_overlap: <平均重複度>
  warning: kpi_overlap > 0.7 の場合、ユーザーに警告
```

### 4.4 L4 運用中モニタリング（必須、自動）

定期実行（日次）で以下を観測:

```yaml
metrics:
  - 各ペルソナの直近30日の発言文体類似度（他ペルソナとの差）
  - 結論一致率（同じ議題に対する判断の重複）
  - 持論変更頻度の分布
  
alert:
  - 文体類似度 > 0.85 が複数ペルソナ間で発生 → 強制差分化プロンプト注入候補
  - 結論一致率が継続的に高い → ペルソナ入れ替え推奨
  - 持論変更が頻繁 → 「浅い理解で持論を変える」（不健全）の可能性検出
```

---

## 5. 機密分類連動の自動格下げ（必須実装）

### 5.1 召喚時の確実な宣言要求

`conclave_summon` の confidentiality は必須パラメータ。省略不可、デフォルト値も持たない（暗黙の PUBLIC 化を防ぐ）。

### 5.2 ライセンス自動格下げ

MEMORY エントリ生成時、confidentiality 値に基づきデフォルト・ライセンスが上書きされる:

```python
# 概念実装
def determine_default_license(confidentiality, layer):
    if confidentiality == "CONFIDENTIAL":
        return "PRIVATE"  # 両層とも PRIVATE
    elif confidentiality == "INTERNAL":
        return "NON_TRANSFERABLE" if layer == "fact" else "READ_ONLY"
    else:  # PUBLIC
        return "PUBLIC" if layer == "fact" else "READ_ONLY"
```

ユーザーが明示的に上書き指定した場合のみ、宣言された confidentiality より「**緩い**」ライセンスを許容（厳格化方向は常に許可）。

### 5.3 EXTERNAL-PUBLIC 昇格の人間レビュー必須

ギルド外への共有（OSS流通など）には個別エントリの EXTERNAL-PUBLIC ライセンス昇格が必要。これは Conclave 内部では自動化せず、人間レビューを通す:

```yaml
conclave_promote_external:
  input:
    memory_entry_id: M-...
    target_license: EXTERNAL_PUBLIC
    human_reviewer: <reviewer-id>
    reason: <昇格理由>
  
  validation:
    - 元の confidentiality が PUBLIC または INTERNAL であること
    - reviewer が昇格権限を持つこと
    - エントリが PRIVATE の場合は昇格不可
```

---

## 6. ピアレビュー機能（A3 防御の完成）

### 6.1 蒸留時の自動ピアレビュー

蒸留3回ごとに、同ギルドの別ペルソナがレビューを実施:

```yaml
conclave_peer_review:
  trigger: distillation_complete
  reviewer: <同ギルドの別ペルソナ>
  review_targets: <蒸留候補>
  
  output:
    sanity_check: ok | suspicious | rejected
    notes: <レビュアーの指摘>
```

ピアレビューで `suspicious` または `rejected` が出た候補は、ユーザーへの通知＋人間判断を経るまで成長層に取り込まれない。

### 6.2 ピアレビューもMEMORY化

ピアレビュー自体も MEMORY エントリとして両ペルソナの growth.md に記録される（事実層 PUBLIC、判断層 READ-ONLY）。

---

## 7. 召喚誘導機能（A2 防御の完成）

### 7.1 ルールベースの誘導

以下の観測可能なルールで誘導を提案:

| 誘導ルール | 発火条件 | 提案ペルソナ |
|---|---|---|
| 長時間同一話題 | 30分以上同じテーマの会話 | ファシリテータ＋議論ロール |
| エラー繰り返し | 同じエラーが3回以上発生 | 専門知識ロール |
| 意思決定タグ | 「決めたい」「迷っている」等のキーワード | 関連する対立軸ペルソナ |
| レビュー依頼 | 「コードレビューして」等の明示 | レビュアー・ペルソナ |

### 7.2 ユーザー制御権

```yaml
user_settings:
  notification_mode: active | subdued | off
  max_per_day: 3                # 控えめデフォルト
  auto_reduce_on_dismiss: true   # 3回連続無視で発火頻度を自動低減
  per_rule_settings: {...}       # ルール単位でON/OFF
```

ユーザーが**いつでも**全提案を1クリックでオフにできる。

### 7.3 自動召喚は実装しない

誘導は**提案**であり、ユーザーの同意で初めて召喚される。提案を経ずに自動的にペルソナを召喚することは行わない（A2 防御原則）。

---

## 8. 定員制度（A1 防御の完成）

### 8.1 上限設定

| 制限 | デフォルト値 | 設定可能範囲 |
|---|---|---|
| 全体ペルソナ数 | 30 | 10-100 |
| 1ギルドあたりペルソナ数 | 7 | 3-15 |
| 同時召喚可能数 | 7 | 2-10 |
| 1ユーザーあたり同時セッション数 | 3 | 1-10 |

### 8.2 上限到達時の動作

新規ペルソナ追加時に上限超過する場合:

```yaml
conclave_add_persona:
  input:
    skill_md_content: ...
  
  on_limit_exceeded:
    error: "Persona limit (30) reached"
    suggestion:
      - 引退候補ペルソナのリスト（出勤回数低下順）
      - 「誰かを引退させてから追加してください」
```

---

## 9. ファシリテータ多重化（A7 防御）

### 9.1 ファシリテータ多重召喚

複数のファシリテータ・ロール（多視点統合型・デザインスプリント型・レトロ型など）を同時召喚可能。互いの整理を批評する:

```yaml
conclave_summon:
  personas: [okada-yuko, design-sprint-facilitator, retro-facilitator]
  facilitator: okada-yuko          # 主進行
  facilitator_critics: [design-sprint-facilitator, retro-facilitator]
```

### 9.2 メタログ

ファシリテータの整理発言は別途メタログに記録される。後で「議論方向に影響したファシリテータ発言」が分析可能:

```yaml
session_meta_log:
  facilitator_interventions:
    - timestamp: ...
      facilitator: okada-yuko
      type: organize | redirect | summarize | propose_consensus
      content: ...
      participants_response: <影響を受けたペルソナとその発言>
```

---

## 10. ペルソナ撤退と凍結（A5 防御）

### 10.1 撤退条件の運用文書化

`docs/withdrawal-criteria.md` を必須文書として配置:

- コア事業 進捗監視のメトリクス
- リソース閾値（工数・予算）
- 凍結条件と凍結手順
- 凍結判定の主体・頻度

### 10.2 凍結API

```yaml
conclave_freeze:
  input:
    target: all | specific_persona-id
    reason: ...
    initiated_by: <human-reviewer-id>
  
  output:
    frozen_at: <timestamp>
    affected_sessions: [...]
    rollback_token: <uuid>     # 後で凍結解除する場合の鍵
```

---

## 11. ギルドとライセンス（自動運用）

### 11.1 ギルド内 MEMORY 共有

ペルソナの growth.md にエントリが追加される際、`license: PUBLIC` であれば自動的に同ギルドのペルソナがアクセス可能になる:

```yaml
conclave_query_guild_memory:
  input:
    requesting_persona: persona-id
    target_guild: guild-id
    query: <検索クエリ>
  
  output:
    entries:
      - memory_entry_id: M-...
        owner_persona: persona-id
        fact: <事実層、PUBLIC/NON_TRANSFERABLE のもの>
        # judgment は要求するペルソナ自身のもの以外は含まれない（READ-ONLY原則）
```

### 11.2 5段階ライセンスの自動制御

各 MEMORY エントリのライセンスに従い、アクセス制御を自動実施:

| ライセンス | 同ギルド読み取り | 同ギルド取り込み | 別ギルド読み取り | 外部 |
|---|---|---|---|---|
| PUBLIC | ✓ | ✓ | ✓ | × |
| READ-ONLY | ✓ | × | ✓（読みのみ） | × |
| NON-TRANSFERABLE | ✓ | ✓ | × | × |
| PRIVATE | × | × | × | × |
| EXTERNAL-PUBLIC | ✓ | ✓ | ✓ | ✓ |

### 11.3 集合的記憶の外部委譲

ギルドを越える集合的記憶は、Memory MCP / UDR にハンドオフ:

```yaml
conclave_export_to_memory_mcp:
  input:
    memory_entry_ids: [M-..., ...]
    target_mcp: memory_mcp_server_url
    license_check: ensure_external_public
```

---

## 12. 説明可能性の3層（API実装）

### 12.1 常時開示エンドポイント（認証不要、組織内）

```
GET /personas/{id}/identity        # コア人格層
GET /personas/{id}/attendance      # 出勤簿
GET /sessions/{id}/minutes         # 議事録
```

### 12.2 要求時開示エンドポイント（認証＋権限確認）

```
GET /personas/{id}/growth?scope=brief|detailed
GET /personas/{id}/recent_summons?days=N
GET /sessions/{id}/full_log
```

### 12.3 非開示の自動redact

- 他組織から取り込んだペルソナの内部 MEMORY
- 他ユーザーが召喚したセッションの詳細
- 舞台裏の生ログのうち、要求権限を超える部分

これらは API レスポンスから自動的に削除され、`redacted_fields` に明示される。

---

## 13. Conclave Persona License（実在モデル対応）

### 13.1 ライセンス雛形

`templates/persona-license.md` を完成版で必須配置。実在の人物を元にしたペルソナを作成する場合、提供者と運用者の権利・義務を明文化:

```yaml
persona_license:
  provider: <提供者名・連絡先>
  scopes:
    thinking_pattern: allowed | not_allowed
    actual_quotes: allowed | not_allowed
    deletion_right: reserved | not_reserved
  
  lifecycle:
    while_active: <提供者意思で削除・更新可能>
    after_retirement: freeze | continue | auto_retire_after_N_days
    after_death:
      family_notification: required
      auto_retire: bool
      continued_use_requires: <別途同意>
  
  external_promotion:
    requires_additional_consent: true   # EXTERNAL-PUBLIC 昇格時
```

### 13.2 ライフサイクル管理API

```yaml
conclave_persona_lifecycle_event:
  input:
    persona: persona-id
    event: retired | deceased | family_request_received
    requested_action: freeze | retire | delete | continue
    documentation: <根拠書類のパス>
```

イベント発生時、自動的に license に従った処理を行う。

---

## 14. 周期階層の自動化

### 14.1 日次（自動）

- 召喚時の日報生成
- KPT差分の状態遷移処理
- 出勤回数のカウント

### 14.2 週次/隔週（自動）

- KPTレトロ集約処理
- 現状KPT導出
- 異質性 L4 中間レポート

### 14.3 月次（自動＋人間レビュー）

- 蒸留候補の生成
- ピアレビューの実行
- ファシリテータ自己点検チェックリスト適用結果の集約
- 解釈到達判定（ユーザー実行）

### 14.4 長期（人間判定）

- 出勤回数低下に基づく休職判定
- 3年休職に基づく引退判定
- ライセンスのライフサイクル変更
- 凍結・特別措置

---

## 15. 第三者レビューの定例化

### 15.1 定例レビュー API

```yaml
conclave_third_party_review:
  input:
    review_target: <設計文書、メモなど>
    reviewers: [tadokoro-takuma, hayashi-chinatsu, hatano-kyoko]  # 商業性・使い手・倫理
    confidentiality: ...
  
  output:
    review_session_id: <uuid>
    findings_by_reviewer: {...}
    aggregated_recommendations: {...}
```

### 15.2 定期実行スケジュール

- 月次定例レビュー（推奨）
- 主要マイルストーン到達時（必須）
- メモの大幅更新時（推奨）

第三者レビュアー3名にはサマリー版・クイックスタート版を事前提供し、設計レビュー版（メモ本書）はリファレンスとして提示する。

---

## 16. ストレステストの定例化

### 16.1 ストレステスト API

```yaml
conclave_stress_test:
  input:
    target_personas: [...]   # 攻撃役を担うペルソナ
    scope: full | targeted
  
  output:
    attacks: [{persona, target_aspect, severity, defense_proposed}, ...]
    coverage_gaps: [...]
    new_required_features: [...]
```

### 16.2 定期実行スケジュール

- 四半期ごと
- 大幅な機能追加時
- インシデント発生後

---

## 17. ストレージスキーマ

### 17.1 主要テーブル

```sql
-- ペルソナ定義
CREATE TABLE personas (
  id TEXT PRIMARY KEY,
  skill_md TEXT NOT NULL,
  growth_md TEXT NOT NULL,
  guild TEXT NOT NULL,
  license TEXT NOT NULL,    -- internal | external_reviewer
  status TEXT NOT NULL,      -- active | frozen | retired | deceased
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

-- セッション
CREATE TABLE sessions (
  id TEXT PRIMARY KEY,
  summoned_by TEXT NOT NULL,
  confidentiality TEXT NOT NULL,
  topic TEXT,
  started_at TIMESTAMP,
  ended_at TIMESTAMP,
  facilitator TEXT,
  duration_minutes INTEGER
);

-- 召喚記録
CREATE TABLE summons (
  id TEXT PRIMARY KEY,
  session_id TEXT REFERENCES sessions(id),
  persona_id TEXT REFERENCES personas(id),
  joined_at TIMESTAMP,
  left_at TIMESTAMP,
  is_facilitator BOOLEAN
);

-- MEMORY エントリ
CREATE TABLE memory_entries (
  id TEXT PRIMARY KEY,
  persona_id TEXT REFERENCES personas(id),
  fact_content TEXT,
  fact_license TEXT,
  judgment_interpretation TEXT,
  judgment_license TEXT,
  superseded_by TEXT REFERENCES memory_entries(id),
  trigger_type TEXT,
  trigger_source TEXT,
  trigger_reasoning TEXT,
  source_session_id TEXT REFERENCES sessions(id),
  created_at TIMESTAMP
);

-- 日報
CREATE TABLE daily_reports (
  id TEXT PRIMARY KEY,
  persona_id TEXT REFERENCES personas(id),
  date DATE,
  yaml_content TEXT,
  session_id TEXT REFERENCES sessions(id)
);
```

### 17.2 全テーブル共通

`project_code` フィールドを全テーブルに含める（既存 Presto 設計と整合）。これにより複数組織が同一サーバーを共有する場合の論理分離を実現。

---

## 18. 認証・権限

### 18.1 ユーザー権限

| 権限 | 内容 |
|---|---|
| `summon` | ペルソナ召喚 |
| `add_persona` | ペルソナ追加（L1/L2 自動チェック適用） |
| `freeze` | ペルソナ凍結 |
| `promote_external` | EXTERNAL-PUBLIC 昇格 |
| `view_growth` | 成長層閲覧（要求時開示） |
| `view_attendance` | 勤怠閲覧（常時開示） |
| `admin` | 全権限 |

### 18.2 組織分離

各組織は `project_code` で論理分離。組織を越えるアクセスは:
- EXTERNAL-PUBLIC ライセンスのエントリのみ可能
- OSS流通は Phase γ で別途設計

---

## 19. MVP からの移行

### 19.1 移行プロセス

1. MVP の `skills/<persona-id>/` ディレクトリを Persona Registry にインポート
2. `attendance/<persona-id>/*.yaml` を daily_reports テーブルにインポート
3. `growth.md` 内の MEMORY エントリを memory_entries テーブルにインポート
4. ライセンスメタデータを各エントリに付与
5. ファイルベース運用と並行運用しながら段階移行

### 19.2 互換性保証

- ファイル形式（YAML/Markdown）は変更しない
- SKILL.md / growth.md の構造は MVP と同一
- ストレージは内部実装、外部 API は YAML/Markdown を返却可能

---

## 20. 完成版の段階的実装計画

### 20.1 Phase β-1（基本機能）

- MCP サーバーの基本実装
- `conclave_summon` / `conclave_dismiss` / `conclave_speak`
- ストレージ層（SQLite）
- 認証（API Key）

### 20.2 Phase β-2（自動化）

- 異質性 L1/L2 自動チェック
- 蒸留半自動化（候補提示）
- ピアレビュー実装
- 説明可能性 API

### 20.3 Phase β-3（完成）

- 異質性 L4 運用中モニタリング
- 召喚誘導機能
- 周期階層の自動化（日次/週次/月次）
- ストレステスト定例化
- 第三者レビュー定例化

### 20.4 Phase γ

- OSS化（エンジン層のみ）
- PostgreSQL 対応
- OAuth2 認証
- マルチ組織対応の本格化

---

## 21. 完成版の成功条件

| 条件 | 必要水準 |
|---|---|
| マルチユーザー運用 | 5名以上が同時利用 |
| 異質性自動担保 | L2/L4 でアラートが適切に発火 |
| 蒸留解釈到達率 | 候補の60%以上で解釈到達 |
| 機密漏洩 | 0件（CONFIDENTIAL データの外部流出ゼロ） |
| ピアレビュー検出率 | 弱い契約事故の50%以上を検出 |
| 第三者レビュー定例実施 | 月次1回以上 |
| ストレステスト定例実施 | 四半期1回以上 |
| 撤退条件遵守 | コア事業 本筋への侵食ゼロ |

---

## 22. 完成版の限界と今後

| 限界 | 対応案 |
|---|---|
| モデル中立性は保証しない | ケースバイケース、組織が選択 |
| ペルソナ依存症の防止は外部課題 | AI業界全体の責任として位置づけ |
| AI倫理の実装は最低限 | 業界共通ガイドライン追従 |

これらは Conclave のスコープ外として明示的に外している。次世代の構想（Phase γ+）で再検討する。

---

## 23. 関連文書

| 文書 | 関係 |
|---|---|
| 全体概要 Spec | 上位文書、用語・思想・スコープ |
| MVP Spec（Skills版） | 前段階、Phase α 対応 |
| 検討メモ v0.4 | 設計判断の根拠 |
| 実測KPI記録 | 完成版でも継続的に更新 |
| メタ・レトロ記録 | 運用知見の蓄積 |
| 撤退条件文書 | A5 防御の運用文書 |

完成版は MVP の拡張であり、思想・用語・スコープは全体概要 Spec と完全整合する。
