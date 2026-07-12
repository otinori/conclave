---
name: conclave-disclosure
description: |
  Conclave のペルソナ・セッションに関する開示要求に応える。ユーザーが
  @conclave disclosure、ペルソナの経歴、成長メモリ、勤怠、議事録、identity、
  またはペルソナがなぜそう振る舞うのかを尋ねたときに使う。
---

# Conclave Disclosure

Conclave の記録を、変更せずに読み取って要約する。

## 開示タイプ

- `identity`: `.conclave/personas/<guild>/<persona-id>/identity.yaml`
- `growth`: `.conclave/personas/<guild>/<persona-id>/growth.yaml`
- `attendance`: `.conclave/attendance/<persona-id>/`
- `minutes`: `.conclave/sessions/<session-id>/minutes.md`
- `session`: `.conclave/sessions/<session-id>/meta.yaml`

## ワークフロー

1. 要求された開示タイプを特定する。
2. 該当するファイルを探す。
3. メタデータおよびファイル内容の機密ラベルを尊重する。
4. ファイルパス付きの簡潔な要約を返す。
5. ユーザーが全文を求めており、そのファイルがローカルのユーザーデータである
   場合、機密区分が制限を示していない限り提供する。

## ルール

- ファイルを編集しない。
- ユーザーの現在のワークスペースの文脈外に機密内容を明かさない。
- データが欠けている場合、どのファイルが期待されていたかを伝える。
