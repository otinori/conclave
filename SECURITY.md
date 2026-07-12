# Security Policy

## 報告方法

脆弱性や機密情報の混入を見つけた場合は、公開 Issue を立てる前に、リポジトリ所有者へ
GitHub の private vulnerability reporting（Security advisories）で連絡してください。

## このプロジェクトの性質

- Conclave はネットワーク通信や認証を行わない、ローカル完結の Skills / 手順書です。
- ユーザーデータ（`.conclave/`）はユーザーのワークスペースに留まり、外部送信されません。
- 同梱フック `hooks/conclave_retro_check.py` はローカルの `.conclave/` を読むのみで、
  書き込み・送信は行いません。

## 利用者への注意

- `.conclave/` 配下に機密情報を置く場合、その workspace の取り扱いに従ってください。
- 本リポジトリには認証情報を含めないでください（`.gitignore` で `.env` / 鍵類を除外済み）。
