#!/usr/bin/env python3
"""Conclave retro-due チェック (Claude Code の SessionStart フック)。

プロジェクトの作業ディレクトリでセッション開始時に実行される。
`.conclave/config.yaml` と `.conclave/retro/state.yaml` を読み、スケジュール
（週次/月次）またはカウンタ方式のレトロスペクティブが必要かどうかを判定し、
必要な場合のみ Claude に `/conclave-retro` の実行を促す SessionStart の
additionalContext メッセージを注入する。

設計方針:
- セッションを絶対にクラッシュさせない: エラーが起きたら黙って exit 0 する。
- 本当に retro が必要なとき以外は無言のままにする（アイドルなワークスペースで
  うるさく催促しない）。
- growth.yaml に関する判断はここでは一切行わない。実際の学習と小/大の
  変化度ゲートはモデルと conclave-retro スキルが担う。

state.yaml のスキーマ (conclave-retro / conclave-dismiss が書き込む):

    schema_version: "1.0"
    last_retro_at: 2026-06-25        # グローバル、任意
    personas:
      <persona-id>:
        summons_since_retro: 2
        last_retro_at: 2026-06-20    # 任意
"""

import json
import os
import sys
from datetime import date, datetime


def _emit(context: str) -> None:
    """SessionStart 向けに additionalContext を注入して終了する。"""
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }))
    sys.exit(0)


def _parse_date(value):
    if value is None:
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    text = str(value).strip()
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(text[:len(fmt) + 2], fmt).date()
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(text).date()
    except ValueError:
        return None


def _load_yaml(path):
    try:
        import yaml  # PyYAML
    except Exception:
        return None
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return yaml.safe_load(fh)
    except Exception:
        return None


def main() -> None:
    root = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    conclave = os.path.join(root, ".conclave")
    if not os.path.isdir(conclave):
        sys.exit(0)  # Conclave ワークスペースではない

    config = _load_yaml(os.path.join(conclave, "config.yaml")) or {}
    retro = (config.get("retro") or {}) if isinstance(config, dict) else {}
    if retro.get("auto") is False:
        sys.exit(0)  # 自動学習が無効

    schedule = retro.get("schedule") or {}
    weekly = bool(schedule.get("weekly"))
    monthly = bool(schedule.get("monthly"))
    threshold = retro.get("trigger_after_n_summons", 3)
    try:
        threshold = int(threshold)
    except Exception:
        threshold = 3

    state = _load_yaml(os.path.join(conclave, "retro", "state.yaml")) or {}
    if not isinstance(state, dict):
        state = {}

    today = date.today()
    reasons = []

    # --- カウンタ方式（retro を行わずにセッションが終了した可能性がある） ---
    due_personas = []
    personas = state.get("personas") or {}
    if isinstance(personas, dict):
        for pid, pstate in personas.items():
            if not isinstance(pstate, dict):
                continue
            try:
                count = int(pstate.get("summons_since_retro", 0))
            except Exception:
                count = 0
            if count >= threshold:
                due_personas.append("%s (%d summons)" % (pid, count))
    if due_personas:
        reasons.append(
            "召喚カウンタが閾値(%d)以上: %s"
            % (threshold, ", ".join(due_personas))
        )

    # --- 時間方式（週次 / 月次） ---
    has_activity = bool(due_personas) or os.path.isdir(
        os.path.join(conclave, "attendance")
    )
    last_global = _parse_date(state.get("last_retro_at"))
    if has_activity and (weekly or monthly):
        if last_global is None:
            reasons.append("retro の記録はまだ無いが勤怠は存在する")
        else:
            age = (today - last_global).days
            if weekly and age >= 7:
                reasons.append("週次 retro が必要（前回から%d日経過）" % age)
            elif monthly and (
                (today.year, today.month) != (last_global.year, last_global.month)
            ):
                reasons.append(
                    "月次 retro が必要（前回: %s）" % last_global.isoformat()
                )

    if not reasons:
        sys.exit(0)  # 何も必要ない — 無言のまま

    _emit(
        "[Conclave] レトロスペクティブが必要なようです: "
        + "; ".join(reasons)
        + "。直近のセッションから自動学習するため /conclave-retro の実行を"
        "検討してください（小さな改善は自動適用、大きな変更は承認待ちに"
        "退避されます）。実行前に .conclave/config.yaml の retro 設定を"
        "再確認してください。これはリマインドであり命令ではありません。"
    )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)
