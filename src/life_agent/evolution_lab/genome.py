from dataclasses import dataclass
import random


@dataclass
class Genome:
    creativity: float = 0.5
    caution: float = 0.5
    sociality: float = 0.5
    exploration: float = 0.5

    def mutate(self, p: float = 0.15, step: float = 0.08):
        for k in ["creativity", "caution", "sociality", "exploration"]:
            if random.random() < p:
                v = getattr(self, k) + random.uniform(-step, step)
                setattr(self, k, max(0.0, min(1.0, v)))


def mendel_pick(a: float, b: float) -> float:
    # Mendel-like random inheritance with midpoint fallback
    r = random.random()
    if r < 0.45:
        return a
    if r < 0.9:
        return b
    return (a + b) / 2


def reproduce(parent_a: Genome, parent_b: Genome) -> Genome:
    child = Genome(
        creativity=mendel_pick(parent_a.creativity, parent_b.creativity),
        caution=mendel_pick(parent_a.caution, parent_b.caution),
        sociality=mendel_pick(parent_a.sociality, parent_b.sociality),
        exploration=mendel_pick(parent_a.exploration, parent_b.exploration),
    )
    child.mutate()
    return child
