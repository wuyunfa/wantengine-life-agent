from dataclasses import dataclass

@dataclass
class FiniteContract:
    life_credit: float
    age_ticks: int
    max_age_ticks: int

    def pass_time(self):
        self.age_ticks += 1
        self.life_credit -= 0.6

    def reward(self,v):
        self.life_credit = min(120.0,self.life_credit+v)

    def alive(self):
        return self.life_credit>0 and self.age_ticks<self.max_age_ticks
