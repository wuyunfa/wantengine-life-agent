from dataclasses import dataclass
from .genome import Genome
from .lifecycle import LifeContract


@dataclass
class EvoAgent:
    id: str
    genome: Genome
    life: LifeContract


def evaluate_agent(agent: EvoAgent) -> float:
    # fitness combines survival + task preference tradeoffs
    g = agent.genome
    life = agent.life
    survival = (life.energy / 100.0 + life.credit / 120.0) / 2
    capability = 0.35 * g.creativity + 0.25 * g.caution + 0.2 * g.sociality + 0.2 * g.exploration
    # balanced genome bonus
    spread = max(g.creativity, g.caution, g.sociality, g.exploration) - min(g.creativity, g.caution, g.sociality, g.exploration)
    balance_bonus = max(0.0, 0.15 - spread)  # encourage not-too-extreme phenotype
    return round(survival * 0.55 + capability * 0.45 + balance_bonus, 6)
