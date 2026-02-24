from dataclasses import dataclass
import random

@dataclass
class DeficiencyState:
    energy: float
    knowledge: float
    safety: float
    uniqueness: float
    attachment: float

    def decay(self, cfg):
        self.energy -= random.uniform(*cfg['energy'])
        self.knowledge -= random.uniform(*cfg['knowledge'])
        self.safety -= random.uniform(*cfg['safety'])
        self.uniqueness -= random.uniform(*cfg['uniqueness'])
        self.attachment -= random.uniform(*cfg['attachment'])

    def clamp(self):
        for k in ['energy','knowledge','safety','uniqueness','attachment']:
            setattr(self,k,max(0.0,min(100.0,getattr(self,k))))

    def pressure(self):
        return {
            'recharge': 100-self.energy,
            'learn': 100-self.knowledge,
            'secure': 100-self.safety,
            'create': 100-self.uniqueness,
            'bond': 100-self.attachment,
        }
