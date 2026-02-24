import csv
import random
import time
from pathlib import Path

from .state import EngineState
from .taskgen import TaskGenerator
from .executor import TaskExecutor


class WantEngine:
    def __init__(self):
        self.speed_factor = 10
        self.state = EngineState()
        self.taskgen = TaskGenerator()
        self.executor = TaskExecutor(enable_openclaw_call=False)

    def calculate_energy_cost(self, complexity: str) -> int:
        base = {"simple": 6, "medium": 8, "complex": 10}.get(complexity, 8)
        variance = random.randint(0, 4)
        fatigue_penalty = 1 + self.state.fatigue / 100
        return int((base + variance) * fatigue_penalty)

    def tick(self, is_executing_task: bool = False) -> None:
        s = self.state
        if s.is_deep_rest:
            target = s.force_rest_recovery_line if s.is_force_rest else s.energy_recovery_line
            s.energy += 0.3 * self.speed_factor
            s.fatigue = max(0.0, s.fatigue - 2 * self.speed_factor)
            if s.energy >= target:
                s.is_deep_rest = False
                s.is_force_rest = False
                s.consecutive_low_energy_ticks = 0
            s.clamp()
            return

        is_low_energy = s.energy < s.energy_healthy_line
        if is_low_energy:
            s.consecutive_low_energy_ticks += 1
            s.fatigue += s.fatigue_growth_per_tick
        else:
            s.consecutive_low_energy_ticks = 0
            s.fatigue = max(0.0, s.fatigue - 0.5 * self.speed_factor)

        if s.consecutive_low_energy_ticks >= s.consecutive_low_energy_limit or s.fatigue >= s.fatigue_critical_line:
            s.is_deep_rest = True
            s.is_force_rest = True
            s.clamp()
            return

        energy_gain = (0.15 if not is_executing_task else 0.1) * self.speed_factor
        boredom_gain = 0.3 * self.speed_factor
        curiosity_gain = 0.25 * self.speed_factor

        if s.energy < s.energy_warning_line:
            s.is_deep_rest = True
            s.clamp()
            return

        s.boredom += boredom_gain
        s.curiosity += curiosity_gain
        s.energy += energy_gain
        s.clamp()

    def get_intention(self):
        s = self.state
        if s.is_deep_rest:
            return "rest", "AI in deep rest", "simple"

        dynamic_safe_energy = s.energy_safe_line + s.fatigue
        if s.energy >= dynamic_safe_energy:
            is_bored = s.boredom > s.boredom_threshold
            is_curious = s.curiosity > s.curiosity_threshold
            if is_bored and is_curious:
                task_type = "boredom" if random.random() < 0.5 else "curiosity"
                act = "action" if task_type == "boredom" else "search"
                task, complexity = self.taskgen.generate(task_type)
                return act, task, complexity
            if is_bored:
                task, complexity = self.taskgen.generate("boredom")
                return "action", task, complexity
            if is_curious:
                task, complexity = self.taskgen.generate("curiosity")
                return "search", task, complexity

        return "wait", "AI stable state | no specific needs now", "simple"

    def run_cycle(self) -> dict:
        s = self.state
        intention_type, intention_text, complexity = self.get_intention()
        executing = False
        success = True

        if intention_type in {"action", "search"}:
            executing = True
            success = self.executor.execute(intention_text)
            if intention_type == "action":
                s.boredom = max(0.0, s.boredom - 35)
            else:
                s.curiosity = max(0.0, s.curiosity - 30)
            s.energy = max(0.0, s.energy - self.calculate_energy_cost(complexity))

        self.tick(is_executing_task=executing)

        return {
            "intention_type": intention_type,
            "task": intention_text,
            "complexity": complexity,
            "energy": round(s.energy, 2),
            "boredom": round(s.boredom, 2),
            "curiosity": round(s.curiosity, 2),
            "fatigue": round(s.fatigue, 2),
            "deep_rest": s.is_deep_rest,
            "success": success,
        }

    def run(self, steps: int = 30, save_csv: bool = True, csv_path: str | None = None):
        rows = []
        for _ in range(steps):
            rows.append(self.run_cycle())
            time.sleep(1 / self.speed_factor)

        if save_csv:
            out = Path(csv_path) if csv_path else Path("outputs") / "want_engine_v02_log.csv"
            out.parent.mkdir(parents=True, exist_ok=True)
            with out.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                writer.writeheader()
                writer.writerows(rows)
            return out
        return None
