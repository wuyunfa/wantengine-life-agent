from dataclasses import dataclass


@dataclass
class EngineState:
    boredom: float = 0.0
    curiosity: float = 0.0
    energy: float = 100.0
    fatigue: float = 0.0
    is_deep_rest: bool = False
    is_force_rest: bool = False
    consecutive_low_energy_ticks: int = 0

    boredom_threshold: float = 60.0
    curiosity_threshold: float = 60.0
    energy_warning_line: float = 25.0
    energy_recovery_line: float = 60.0
    energy_safe_line: float = 40.0
    energy_healthy_line: float = 70.0

    fatigue_growth_per_tick: float = 1.0
    fatigue_critical_line: float = 20.0
    consecutive_low_energy_limit: int = 15
    force_rest_recovery_line: float = 80.0

    def clamp(self) -> None:
        self.boredom = max(0.0, min(100.0, self.boredom))
        self.curiosity = max(0.0, min(100.0, self.curiosity))
        self.energy = max(0.0, min(100.0, self.energy))
        self.fatigue = max(0.0, min(100.0, self.fatigue))
