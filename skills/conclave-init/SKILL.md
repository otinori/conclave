---
name: conclave-init
description: |
  ローカルの Conclave ワークスペースを初期化する。ユーザーが @conclave init を
  求めたとき、.conclave/ を作成したいとき、または Conclave MVP 向けの初期
  config・ギルドフォルダ・勤怠・セッション・retro ディレクトリが必要なときに
  使う。
---

# Conclave Init

現在のプロジェクトワークスペースに、ユーザー所有の `.conclave/` データを作成する。

## ワークフロー

1. `templates/` を含む plugin root を特定する。
2. `.conclave/` が既に存在する場合、その内容を確認し既存のユーザーデータを
   保持する。
3. 不足しているディレクトリを作成する:
   - `.conclave/personas/`
   - `.conclave/personas/architecture/`
   - `.conclave/personas/ops/`
   - `.conclave/personas/field/`
   - `.conclave/personas/governance/`
   - `.conclave/personas/strategy/`
   - `.conclave/personas/facilitation/`
   - `.conclave/personas/business/`
   - `.conclave/personas/ethics/`
   - `.conclave/attendance/`
   - `.conclave/sessions/`
   - `.conclave/retro/`
4. `.conclave/config.yaml` が既に存在しない場合に限り、
   `templates/config.yaml.template` から作成する。
5. どのファイルが新規作成され、どの既存ファイルがそのまま残されたかを
   ユーザーに伝える。

## ルール

- ユーザーが明示的に求めない限り、既存の `.conclave/` ファイルを絶対に
  上書きしない。
- `.conclave/` は plugin データではなくユーザーデータとして扱う。
- ユーザーが変更しない限り、MVP では通知モードを `off` のままにする。
