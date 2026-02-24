from datetime import datetime, timedelta
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from life_agent.autonomy import (  # noqa: E402
    PulseConfig,
    PulseState,
    should_emit_heartbeat,
    should_emit_milestone,
    build_status_message,
)


def test_pulse_heartbeat_logic():
    now = datetime.now()
    cfg = PulseConfig(heartbeat_minutes=15)
    state = PulseState(last_heartbeat_at=now - timedelta(minutes=16))
    assert should_emit_heartbeat(now, state, cfg) is True


def test_milestone_logic_and_message():
    assert should_emit_milestone(True) is True
    msg = build_status_message("M4", "in_progress", "11 passed", "abc123")
    assert "M4" in msg and "commit=abc123" in msg
