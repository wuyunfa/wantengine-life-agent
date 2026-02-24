from pathlib import Path
from datetime import datetime, timedelta
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from life_agent.autonomy import PulseConfig, PulseState, should_emit_heartbeat, build_status_message


def main():
    now = datetime.now()
    cfg = PulseConfig(heartbeat_minutes=15)
    state = PulseState(last_heartbeat_at=now - timedelta(minutes=20))

    emit = should_emit_heartbeat(now, state, cfg)
    status = build_status_message("M4", "pulse_demo", "pending")

    out = ROOT / "outputs" / "autonomy_pulse_demo.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({"emit": emit, "status": status}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"done: {out}")


if __name__ == "__main__":
    main()
