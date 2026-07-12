---
name: conclave-push-persona
description: |
  現在のプロジェクトスコープのペルソナを、ユーザースコープ (~/.conclave) または
  名前付きの git バックエンドバンク (--bank <name>, sync.banks.<name>、例:
  conclave_persona-bank) へ同期する。ユーザーがこのプロジェクトで育てた
  ペルソナをエクスポート・共有したいときに使う。イメージは "git push" —
  プロジェクトが取得元、ユーザースコープまたはバンクが取得先。--bank 指定時は
  そのバンクのローカル clone に対して実際の git add/commit/push まで行う。
---

# Conclave Push Persona

プロジェクトで育てたペルソナを同期する。宛先は 2 種類:

- 既定: ユーザースコープ (`sync.user_scope`, 既定 `~/.conclave`)。ファイル
  コピーのみで完結する、machine-local な個人プール。
- `--bank <bank-name>`: `sync.banks.<bank-name>` に登録された git リモート
  付きの共有バンク（例: `conclave_persona-bank`）。ファイル同期に加えて
  `conclave-bank-sync` 経由で実際に `git commit` / `git push` まで行う。

git push のイメージ: プロジェクト（ローカル）→ ユーザースコープ or バンク（リモート）。

## 入力

以下のいずれかを受け付ける:

- `--persona <id>`: 単一ペルソナを対象
- `--guild <guild>`: ギルド内の全ペルソナを対象
- `--bank <bank-name>`: 宛先をユーザースコープではなく指定バンクにする
- 引数なし: プロジェクト内の全ペルソナを候補として表示し、人間が選択

## ワークフロー

1. `.conclave/config.yaml` を読む。以下を決定する:
   - `sync.user_scope`（既定: `~/.conclave`）
   - `sync.conflict_strategy`（既定: `stop`）
   - 宛先パス `<target>`:
     - `--bank <bank-name>` が指定された場合: `sync.banks.<bank-name>` を
       解決できなければ停止し、設定済みバンク一覧を提示する。解決できたら
       `conclave-bank-sync --bank <bank-name> --mode pull` を実行し、
       `<target>` = バンクの clone パスとする。この pull が停止した場合
       (history 分岐・未コミット変更あり)、push 全体を中止する。
     - 指定なし: `<target>` = `sync.user_scope`（git 操作は行わない）。

2. `.conclave/personas/<guild>/<persona-id>/` から対象ペルソナを解決する。

3. 各対象ペルソナについて:

   a. **L1 検証**: `identity.yaml` に必須フィールド（`id`, `description`,
      `guild`, `license`, `kpis`, `role`, `expertise`）が全て揃っているか
      確認する。欠けているフィールドがあれば報告し、そのペルソナをスキップする。

   b. **宛先の確認**: `<target>/personas/<guild>/<persona-id>/` を探す。

   c. **ペルソナが宛先に存在しない場合**:
      - `identity.yaml` → `<target>/personas/<guild>/<id>/identity.yaml` に
        コピーする
      - コピーした identity に `derived_from` の同期記録を追記する:
        ```yaml
        derived_from:
          source: <project-path>/.conclave/personas/<guild>/<id>
          synced_at: <ISO-date>
          direction: push
        ```
      - `growth.yaml`（存在する場合）をそのまま宛先にコピーする。
      - **追加**としてマークする。

   d. **ペルソナが宛先に既に存在する場合**:
      - **identity.yaml**: 主要フィールドを比較する。異なる場合は diff を
        表示し、**停止する**（人間承認なしに上書きしない）。ユーザーに尋ねる:
        「宛先の identity が異なります。上書きしますか? [y/N]」。`y` の場合の
        み進める。
      - **growth.yaml**: エントリ単位でマージする:
        - プロジェクトと宛先の両方の `growth.yaml` を読む。
        - プロジェクトの growth の各エントリについて:
          - `id` が宛先の growth に無い → 追記（**追加**とマーク）。
          - `id` が存在し内容が同一 → スキップ（**スキップ**とマーク）。
          - `id` が存在し内容が異なる → `conflict_strategy` を適用する:
            - `stop`: 停止し、競合しているエントリを報告し、人間を待つ。
            - `skip`: 宛先版を維持し、**スキップ**とマークする。
            - `ask`: diff を表示し、ユーザーにプロジェクト版 / 宛先版 /
              手動 を選ばせる。

4. 宛先の `identity.yaml` に同期の来歴を追記する:
   ```yaml
   derived_from:
     source: <project-path>/.conclave/personas/<guild>/<id>
     synced_at: <ISO-date>
     direction: push
   ```
   同一ソースから `direction: push` の `derived_from` が既に存在する場合、
   `synced_at` のみ更新する。

5. **`--bank <bank-name>` が使われた場合**、変更をリモートへ反映する:
   - 手順 3/4 で実際に触れた相対パスを集める（追加または変更された persona
     ディレクトリのみ — バンク全体は絶対に含めない）。
   - 何も触れていない場合（全ペルソナがスキップされた場合）、その旨を報告し
     git 手順は完全にスキップする — 空コミットは作らない。
   - それ以外は `conclave-bank-sync --bank <bank-name> --mode commit-push` を、
     それらのパスと
     `growth: <persona-ids> from <project-name>` のようなメッセージで実行する。
   - この手順が停止した場合（リトライ後も push が拒否された、rebase が
     conflict した）、バンク clone の状態を報告し停止する — ローカルの宛先
     ファイルは既に更新済みだが、リモートへの push は手動解決が必要。

6. 完了レポートを表示する:
   ```
   ## Push Persona レポート

   対象: <N> ペルソナ
   宛先: <sync.user_scope または --bank で指定したバンク名>

   | ペルソナ | identity | growth 追加 | growth スキップ | 要確認 |
   |---|---|---|---|---|
   | <id> | 新規 / 更新 / スキップ | N | N | N |

   完了。同期先: <target>
   <--bank 使用時のみ> commit: <sha>  push: <remote>/<branch>
   ```

## ルール

- 宛先の growth.yaml のエントリを自動的に削除・上書きしない。
- 既存の `derived_from` 履歴を常に保持する。追記のみで置き換えない。
- L1 検証に失敗した場合、そのペルソナはスキップし残りを続行する。
- `conflict_strategy: stop` かつ競合がある場合、push 全体を停止し全ての
  競合エントリを報告し、人間の解決を待つ。
- `--bank` の push では、この実行で触れた特定の persona パスのみを
  `git add` する。バンク clone 内の無関係な変更をステージ・コミットしない。
- Conclave は判断材料を提供するだけであり、ユーザーに代わって決定はしない。
