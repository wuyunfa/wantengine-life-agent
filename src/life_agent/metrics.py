from dataclasses import dataclass


@dataclass
class LifeMetrics:
    mpi: float = 0.0  # Motivation Persistence Index
    fpas: float = 0.0  # Finite-Pressure Adaptation Score
    mcr: float = 0.0  # Meaning Coherence Ratio
    asi: float = 0.0  # Attachment Selectivity Index


def calc_mpi(actions: list[str]) -> float:
    if not actions:
        return 0.0
    active = sum(1 for a in actions if a in {"learn", "create", "secure", "bond", "recharge"})
    return round(active / len(actions), 4)


def calc_fpas(avg_life_credit: float) -> float:
    # normalize around target 80
    return round(max(0.0, min(1.0, avg_life_credit / 80.0)), 4)


def calc_mcr(missions: list[str]) -> float:
    if not missions:
        return 0.0
    key_words = ["主动", "恢复", "产出", "守护", "风险"]
    hit = sum(1 for m in missions if any(k in m for k in key_words))
    return round(hit / len(missions), 4)


def calc_asi(bond_first_count: int, total_rounds: int) -> float:
    if total_rounds <= 0:
        return 0.0
    return round(bond_first_count / total_rounds, 4)
