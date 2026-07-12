---
description: 類似ペルソナを統合する（2→1）、または1体を特化ペルソナへ分割する（1→2）
argument-hint: "--merge <id-A> <id-B> | --split <id>"
---

`conclave-merge-persona` スキルを使い、重複したペルソナを整理する、または
特化した役割を切り出す。同一人物が作成・指示したペルソナに限り機能する。

`skills/conclave-merge-persona/SKILL.md` のワークフローに従うこと:

**統合モード** (`--merge <id-A> <id-B>`):
1. 同一所有者であることを確認する。
2. identity の差分を並べて表示する。
3. 統合後の identity 案を提示し、人間の承認を待つ。
4. 統合結果に L1/L2 チェックを実施する。
5. どちらの id を残すか尋ねる（A / B / 新規）。
6. growth.yaml のエントリを統合し、コンフリクトは対話的に解決する。
7. 廃止するペルソナを `deprecated_by` 注記付きでアーカイブする。

**分割モード** (`--split <id>`):
1. 元ペルソナの kpis と expertise を分析する。
2. 2体の特化ペルソナ案を提示し、人間の承認を待つ。
3. 新しい id とギルドを尋ねる。
4. 新規2体それぞれに L1/L2 チェックを実施する。
5. growth.yaml の各エントリの振り分け案を提示し、人間の確認を待つ。
6. 新しい identity.yaml と growth.yaml を書き込む。
7. 元ペルソナを `deprecated_by: [A, B]` 注記付きでアーカイブする。

ユーザー入力: $ARGUMENTS
