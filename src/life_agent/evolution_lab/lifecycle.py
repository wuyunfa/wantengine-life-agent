from dataclasses import dataclass


@dataclass
class LifeContract:
    energy: float = 100.0
    age: int = 0
    max_age: int = 80
    credit: float = 100.0

    def tick(self):
        self.age += 1
        self.energy -= 1.8
        self.credit -= 0.8
        self.energy = max(0.0, self.energy)
        self.credit = max(0.0, self.credit)

    def reward(self, value: float):
        self.credit = min(120.0, self.credit + value)

    def alive(self) -> bool:
        return self.energy > 0 and self.credit > 0 and self.age < self.max_age
