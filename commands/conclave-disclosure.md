---
description: Conclave の記録（identity・growth・attendance・minutes・session）を開示する
argument-hint: persona: <persona-id>, type: identity|growth|attendance|minutes|session
---

`conclave-disclosure` スキルを使い、Conclave の記録を変更せずに読み取り・要約する。

`skills/conclave-disclosure/SKILL.md` のワークフローに従うこと:

開示タイプ:
- `identity`: `.conclave/personas/<guild>/<persona-id>/identity.yaml`
- `growth`: `.conclave/personas/<guild>/<persona-id>/growth.yaml`
- `attendance`: `.conclave/attendance/<persona-id>/`
- `minutes`: `.conclave/sessions/<session-id>/minutes.md`
- `session`: `.conclave/sessions/<session-id>/meta.yaml`

1. 要求された開示タイプを特定する。
2. 該当するファイルを探す。
3. メタデータおよびファイル内容の機密区分を尊重する。
4. ファイルパス付きの簡潔な要約を返す。
5. ユーザーがローカルユーザーデータの全文を求めた場合、機密区分による制限が
   なければ提供する。

ファイルを編集しないこと。ユーザーの現在のワークスペース外へ機密内容を開示しない
こと。データが見つからない場合は、どのファイルを想定していたかを伝えること。

ユーザー入力: $ARGUMENTS
