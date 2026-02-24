from .arena import EvoAgent, evaluate_agent
from .genome import reproduce
from .lifecycle import LifeContract


def next_generation(population: list[EvoAgent], keep_ratio: float = 0.4) -> list[EvoAgent]:
    scored = sorted([(evaluate_agent(a), a) for a in population], key=lambda x: x[0], reverse=True)
    keep_n = max(2, int(len(population) * keep_ratio))
    elites = [a for _, a in scored[:keep_n]]

    children = []
    idx = 0
    while len(elites) + len(children) < len(population):
        p1 = elites[idx % len(elites)]
        p2 = elites[(idx + 1) % len(elites)]
        child_gene = reproduce(p1.genome, p2.genome)
        child = EvoAgent(
            id=f"gen_child_{idx}",
            genome=child_gene,
            life=LifeContract(),
        )
        children.append(child)
        idx += 1

    return elites + children
