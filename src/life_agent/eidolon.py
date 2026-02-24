from dataclasses import dataclass
import random

@dataclass
class Gene:
    creativity_bias: float=0.5
    caution_bias: float=0.5

    def mutate(self):
        self.creativity_bias=max(0,min(1,self.creativity_bias+random.uniform(-0.05,0.05)))
        self.caution_bias=max(0,min(1,self.caution_bias+random.uniform(-0.05,0.05)))

def reproduce(a: Gene, b: Gene):
    c = Gene(
        (a.creativity_bias + b.creativity_bias) / 2,
        (a.caution_bias + b.caution_bias) / 2,
    )
    c.mutate()
    return c
