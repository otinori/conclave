---
name: conclave-fork-persona
description: |
  既存の Conclave ペルソナを新規ペルソナへ fork する。ユーザーが
  @conclave fork-persona を求めたとき、サンプル/コミュニティ由来のペルソナを
  派生させたいとき、または derived_from の追跡付きで独立した空の成長メモリが
  必要なときに使う。
---

# Conclave Fork Persona

差異を保ちながら、既存の identity から新規ペルソナを作成する。

## ワークフロー

1. パスまたはサンプル id で元ペルソナを特定する。
2. 元の `identity.yaml` を読む。
3. 対象の `id` と `guild` を収集する。
4. 少なくとも 1 件の KPI 変更を必須とする。KPI の完全一致は禁止する。
5. role・profile・speech style の変更を促す。
6. `$conclave-create-persona` と同じ L1・L2・容量チェックを実行する。
7. 対象の `identity.yaml` を以下の内容で書き込む:

```yaml
derived_from:
  source: "<source path>"
  forked_at: "<YYYY-MM-DD>"
  changes_from_source:
    - kpis
```

8. 新規の空 `growth.yaml` を書き込む。

## ルール

- 元の `growth.yaml` を絶対にコピーしない。
- 元ファイルを保持する。
- 対象 id が既に存在する場合は停止し、新しい id を求める。
