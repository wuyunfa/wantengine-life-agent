from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class PulseConfig:
    heartbeat_minutes: int = 15


@dataclass
class PulseState:
    last_milestone_at: datetime | None = None
    last_heartbeat_at: datetime | None = None


def should_emit_milestone(progress_changed: bool) -> bool:
    return progress_changed


def should_emit_heartbeat(now: datetime, state: PulseState, cfg: PulseConfig) -> bool:
    if state.last_heartbeat_at is None:
        return True
    return now - state.last_heartbeat_at >= timedelta(minutes=cfg.heartbeat_minutes)


def build_status_message(module: str, stage: str, tests: str, commit: str | None = None) -> str:
    base = f"[{module}] {stage} | tests={tests}"
    return f"{base} | commit={commit}" if commit else base
