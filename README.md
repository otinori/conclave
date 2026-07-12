# Conclave

Conclave は、複数の専門化された AI ペルソナを必要な場面で召喚し、ペルソナ同士で議論させる、Skills ベースの MVP です。

**Status**: Phase alpha（個人検証向け MVP）
**License**: MIT

---

## 概要

### 開発動機

多くの AI エージェントは単一人格で応答するため、意見の異質性（heterogeneity）が
均質化されやすい。一方で、サーバーや MCP 通信を前提にした本格的なマルチエージェント
基盤は導入コストが高く、「必要な場面で異なる立場の意見を素早く集める」という
軽量なニーズには過剰である。Conclave は、サーバーレスで Codex / Claude Code の
Skills 機構だけを使い、「異質性のオンデマンド供給」という思想が最小構成で
機能するかを検証するために作られた。

### ゴール

- 人間が議題と機密分類を宣言し、必要なペルソナだけを召喚できるようにする
- 各ペルソナが異なる KPI・立場・口調で意見を出し、判断材料の幅を広げる
- セッションの記録（日報・議事録）をローカルに残し、後から開示できるようにする
- 蒸留は候補提示にとどめ、人間が解釈到達を確認してから `growth.yaml` に反映する
- レトロスペクティブでは、小さな改善はペルソナ自身の解釈で自動学習し、
  大きな変更（持論の反転・ライセンス格上げ等）は人間承認に回す
- 最終判断と責任は常に人間に残す（Conclave は決定機構ではなく支援機構）

### 今できること

- Codex / Claude Code の両方にプラグインとしてインストールできる
  （`skills/` と `templates/` は共有、plugin manifest のみ分離）
- 14 個の engine skills（召喚・帰宅・蒸留・レトロ・ペルソナ作成/fork/設計・開示・
  ペルソナ同期・統廃合・バンク連携）と 16 個の slash command
- ペルソナを `~/.conclave`（ユーザースコープ）や git バンクへ push/pull し、
  プロジェクトを越えて育てたペルソナを再利用できる
- レトロスペクティブの自動学習（小さな改善は自動、大きな変更は人間承認待ち）
- retro リマインドの native SessionStart フック（marketplace 経由なら追加設定不要）

### 今後やりたいこと

- Codex plugin としての実ランタイム動作確認（JSON manifest の妥当性は確認済み）
- Skill frontmatter の一括 validator 実行
- SessionStart フックの実セッションでの発火確認
- `.conclave/` 初期化の別 workspace での end-to-end テスト
- 配布サンプル persona の拡充（現状 `sample-facilitator` 1 名のみ）
- Phase β 以降の MCP 化（[docs/design/spec/SPEC-0003-final.md](docs/design/spec/SPEC-0003-final.md)）

### 現在の状態

Phase alpha（個人検証向け MVP）。現行バージョンは `0.6.0.1-PoC`。
配布パッケージ一式（plugin manifest・marketplace・14 skills・16 commands・
native フック・テンプレート・サンプル）は揃っているが、実ランタイムでの
E2E 検証は一部未実施（詳細は [HANDOVER.md](HANDOVER.md) を参照）。

---

## 動作環境

### 前提条件

導入前に以下を確認してください。

#### 必須

| 項目 | 要件 |
|---|---|
| AI エージェント CLI | 下記いずれか 1 つ以上: **Claude Code**（Skills 機能対応版、marketplace 推奨）/ Codex CLI（local plugin として利用） |
| Git リポジトリ | 対象 workspace が Git 管理下にあること（`.conclave/` の永続化・バージョン管理を前提とする） |

#### 任意（機能ごと）

| 機能 | 追加要件 |
|---|---|
| ペルソナバンク（`--bank <name>`、`conclave-push-persona` / `conclave-pull-persona` / `conclave-bank-sync`） | `git` CLI と、バンクのリモートへの push 権限がある環境。force push は行わず、履歴が分岐した場合は必ず人間の判断を待つ |
| retro リマインドの native フック（`hooks/hooks.json`） | Claude Code のプラグイン機構（marketplace / ローカル plugin 有効化時に自動で効く）。`python3` が PATH にある環境（標準ライブラリのみで完結、PyYAML 等の追加パッケージは不要）。`python3` が無い環境でもエラーにはならず、フックが無言で no-op するだけ |
| retro リマインドの手動フック（`/conclave-hook-install`） | 手動 clone や Codex 利用時のフォールバック。settings.json への書き込み権限が必要。python3 の要否は native フックと同じ |

> `skills/*/SKILL.md` は AI エージェントが読んで実行する手順書であり、実行コードではない。
> Conclave の中核機能（召喚・記録・蒸留等）に Python は一切不要。Python3 が関わるのは
> 上記の retro リマインドフック（任意機能）だけ。

#### 不要なもの

- **外部 API キー・有料サービスは一切不要。** `skills/` は手順書ベースの MVP 実装であり、LLM 外部呼び出し・embedding・ベクトル DB への依存を持たない
- **npm / pip 等のパッケージインストールは不要。** `package.json` / `requirements.txt` 等のマニフェスト自体が存在しない
- **サーバー・MCP 通信は不要。** Codex plugin / Claude Code plugin と `SKILL.md` 群だけで完結する（Phase γ 以降の MCP 化は [SPEC-0003-final.md](docs/design/spec/SPEC-0003-final.md) 参照）

### 対応プラットフォーム

Codex CLI と Claude Code の両方に対応。プラグイン配布物としてインストールでき、
OS 依存の制約はない。

---

## クイックスタート

### Codex

1. このフォルダを Codex のローカル plugin として使う
2. 対象 workspace で `$conclave-init` を実行する
3. `$conclave-create-persona` でペルソナを対話式に作成する（`.conclave/personas/<guild>/<persona-id>/` に `identity.yaml` / `growth.yaml` が生成される。既存ペルソナを流用する場合は `$conclave-fork-persona`）
4. `$conclave-summon` で議論を開始する
5. `$conclave-dismiss` で記録を生成する
6. 必要に応じて `$conclave-distill` と `$conclave-distill-accept` で成長層を更新する

### Claude Code

marketplace 経由（推奨・クローン不要）:

```text
/plugin marketplace add otinori/conclave
/plugin install conclave@conclave
```

有効化すると skills・commands に加えて retro リマインドの SessionStart フックが
native に自動で効く（`.conclave/` の無い workspace では無言）。

ローカル plugin として使う場合:

1. このフォルダを Claude Code のローカル plugin として使う
2. 対象 workspace で `/conclave-init` を実行する
3. `/conclave-create-persona` でペルソナを対話式に作成する（`.conclave/personas/<guild>/<persona-id>/` に `identity.yaml` / `growth.yaml` が生成される。既存ペルソナを流用する場合は `/conclave-fork-persona`）
4. `/conclave-summon` で議論を開始する
5. `/conclave-dismiss` で記録を生成する
6. 必要に応じて `/conclave-distill` と `/conclave-distill-accept` で成長層を更新する

---

## 主な使い方

```text
/conclave-init
この workspace に Conclave を初期化して。
```

```text
/conclave-summon
personas: [sato-kenichi, yamamoto-takuya]
confidentiality: INTERNAL
topic: スプリント実装方針をレビューしたい
```

```text
/conclave-dismiss
このセッションを終了して、日報と議事録を生成して。
```

詳しい操作例・全コマンドの対応表は [docs/manual/usage.md](docs/manual/usage.md) を参照してください。

### Skill 一覧

Codex では `$conclave-xxx`、Claude Code では `/conclave-xxx` で呼び出します。

- `conclave-init` - workspace に `.conclave/` を初期作成
- `conclave-summon` - ペルソナを召喚してセッション開始（`--bank <name>` で指定バンクから取り込んでから召喚）
- `conclave-dismiss` - セッション終了、日報・議事録生成
- `conclave-distill` - 日報から memory 候補を提示
- `conclave-distill-accept` - 解釈到達済み memory を `growth.yaml` に追記
- `conclave-retro` - レトロスペクティブで自動学習（小さな改善は自己解釈で自動追記、大きな変更は承認待ちに退避）
- `conclave-create-persona` - 対話式に新規ペルソナ作成
- `conclave-fork-persona` - 既存ペルソナを fork
- `conclave-design-persona` - ペルソナ設計会議で新規ペルソナ作成
- `conclave-disclosure` - identity / growth / attendance / minutes の開示
- `conclave-push-persona` - プロジェクトのペルソナをユーザースコープ（`~/.conclave`）または `--bank` で指定した git バンクへ同期
- `conclave-pull-persona` - ユーザースコープのペルソナをプロジェクトへマージ
- `conclave-merge-persona` - 同一所有者のペルソナを統合（2→1）または分割（1→2）
- `conclave-bank-sync` - 名前付きペルソナバンク（`sync.banks.<name>`）のローカル clone を pull / commit+push する git 連携（`conclave-summon` / `conclave-push-persona` の `--bank` から内部的に呼ばれる）

加えて Claude Code 専用の slash command が 2 つあります（skill ではなく
settings 操作コマンド）。marketplace / 有効化済み plugin では retro フックが
native で効くため通常は不要で、手動 clone や Codex 利用時のフォールバックです。

- `/conclave-hook-install` - retro リマインドの SessionStart フックを settings に設定
- `/conclave-hook-uninstall` - そのフックを解除

### ペルソナのスコープと移動

ペルソナは 3 つのスコープ（置き場）のどれかに存在し、コマンドで移動・複製
できます。**プロジェクトスコープが常にハブ**で、ユーザースコープとペルソナ
バンクはプロジェクトを介してのみやり取りします（ユーザースコープとバンクが
直接同期することはありません）。

```text
ユーザースコープ                プロジェクトスコープ              ペルソナバンク
(~/.conclave/personas/)         (<project>/.conclave/personas/)   (sync.banks.<name> の git remote)
個人限定・非git                  ← 全 skill の起点（ハブ）           複数プロジェクト/人で共有

        pull-persona ─────────────►│
        ◄───────────── push-persona│
                                    │
                                    │◄───────── summon --bank（取り込んでから召喚）
                                    │──────────► push-persona --bank（bank-sync 経由で commit/push）
```

| したいこと | コマンド | 移動方向 |
|---|---|---|
| 他プロジェクトで育てたペルソナを持ち込む | `conclave-pull-persona` | ユーザースコープ → プロジェクト |
| このプロジェクトのペルソナを個人プールに書き戻す | `conclave-push-persona` | プロジェクト → ユーザースコープ（既定の宛先） |
| 共有バンクのペルソナを使って議論する | `conclave-summon --bank <name>` | ペルソナバンク → プロジェクト（取り込んでから召喚） |
| このプロジェクトの成長をチームと共有する | `conclave-push-persona --bank <name>` | プロジェクト → ペルソナバンク（`git commit`/`push` まで実行） |
| バンクの clone 自体を最新化する | `conclave-bank-sync` | ペルソナバンク ⇄ ローカル clone（他コマンドから内部的にも呼ばれる） |

### Persona Bank

ペルソナは `--bank <name>` を使うことで、プロジェクトを越えて git リモートで
共有・成長させられます。既定で 1 つのバンクが登録済みです
（`templates/config.yaml.template`）:

```yaml
sync:
  banks:
    persona-bank:
      remote: https://github.com/otinori/conclave_persona-bank
      path: ~/.conclave/banks/persona-bank
```

- 召喚: `/conclave-summon --bank persona-bank personas: [...] ...` — バンクから
  ペルソナ（identity.yaml / growth.yaml）を取り込んでから召喚する。
- 書き戻し: `/conclave-push-persona --bank persona-bank --persona <id>` —
  growth.yaml の成長を含めてバンクの clone に反映し、`git commit` / `git push`
  まで実行する。
- バンクとの git 連携（clone / pull / commit / push）は `conclave-bank-sync`
  が担う。force push は行わず、history が分岐した場合は必ず人間の判断を待つ。
- `sync.user_scope`（既定 `~/.conclave`）は個人限定・非 git の領域として
  意図的にバンクとは分離している。CONFIDENTIAL セッション由来の成長などを
  誤って共有バンクに push しないための境界になる。

---

## 構成

```text
conclave/
  .codex-plugin/plugin.json
  .claude-plugin/plugin.json
  .claude-plugin/marketplace.json
  skills/
  commands/
  hooks/
  templates/
  samples/.conclave-sample/
  docs/
    design/        # 仕様 (spec/) ・構成 (architecture.md)
    manual/         # 使い方 (usage.md / install.md ほか)
    ops/            # 運用・撤退条件・実測KPI
```

主な構成:

- `.codex-plugin/plugin.json` - Codex plugin manifest
- `.claude-plugin/plugin.json` - Claude Code plugin manifest
- `.claude-plugin/marketplace.json` - Claude Code marketplace カタログ（この repo を 1 plugin として配布）
- `skills/` - Conclave エンジン Skills（Codex / Claude Code 共通、計 14）
- `commands/` - Claude Code 用 slash commands（`/conclave-init` など、計 16）
- `hooks/` - retro リマインドの native フック（`hooks.json` と判定スクリプト）
- `templates/` - `.conclave/` 用テンプレート
- `samples/.conclave-sample/` - 最小サンプル workspace
- `docs/design/` - 仕様（`spec/`）・構成（`architecture.md`）・設計メモ
- `docs/manual/` - 使い方（`usage.md`）・インストール（`install.md`）・作成ガイド
- `docs/ops/` - 運用・撤退条件・実測 KPI

### User Data Boundary（配布物とユーザーデータの分離）

Plugin 配布物とユーザーデータは分離します。

- 更新してよい配布物: `skills/`, `templates/`, `docs/`, `samples/`
- 保護するユーザーデータ: workspace 側の `.conclave/`（`.gitignore` 対象、本リポジトリには含まれない）

Plugin のアップグレード時に `.conclave/` を上書きしないでください。

---

## ドキュメント

- [docs/design/architecture.md](docs/design/architecture.md) - 構成（現在形）
- [docs/design/spec/SPEC-0001-overview.md](docs/design/spec/SPEC-0001-overview.md) - 全体概要
- [docs/design/spec/SPEC-0002-mvp.md](docs/design/spec/SPEC-0002-mvp.md) - Skills 版 MVP 仕様
- [docs/design/spec/SPEC-0003-final.md](docs/design/spec/SPEC-0003-final.md) - 将来の MCP 化仕様
- [docs/manual/usage.md](docs/manual/usage.md) - 使い方ガイド
- [docs/manual/install.md](docs/manual/install.md) - インストール手順
- [docs/manual/persona-authoring.md](docs/manual/persona-authoring.md) - ペルソナ作成ガイド
- [docs/manual/first-usecase.md](docs/manual/first-usecase.md) - 最初のユースケース
- [docs/manual/retro-auto-learning.md](docs/manual/retro-auto-learning.md) - レトロ自動学習（v0.2 拡張）
- [docs/ops/measured-kpi.md](docs/ops/measured-kpi.md) - 実測 KPI
- [docs/ops/withdrawal-criteria.md](docs/ops/withdrawal-criteria.md) - 撤退条件

---

## マルチエージェント協働

本リポジトリで作業する AI エージェント向けの共通ポリシーは [AGENTS.md](AGENTS.md) を参照。

利用者のセッション記録（勤怠・議事録・成長層メモリ）は配布物に含まれない
workspace 側 `.conclave/` に生成され、`conclave-disclosure` skill が開示窓口となる。

---

## ライセンス

MIT License で公開しています。詳細は [LICENSE](LICENSE) を参照してください。

---

## 謝辞

- **[Claude Code](https://claude.com/claude-code)**（Anthropic）/ **Codex CLI**（OpenAI）— 本プロジェクトが Skills 機構の実装対象とする AI エージェント CLI。サーバーや MCP 通信を持たずに「異質性のオンデマンド供給」を検証できるのは、両ツールの skills / slash command 機構があってこそ

コードレベルの外部ライブラリ依存は持たない（[前提条件](#前提条件)参照）ため、
上記は「思想的な参考・連携先」としての記載であり、ビルド・実行時の第三者コード同梱はない。
