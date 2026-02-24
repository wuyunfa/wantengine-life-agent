from dataclasses import dataclass, field
import random
from .vitalis import DeficiencyState
from .finis import FiniteContract
from .eidolon import Gene
from .attachment import AttachmentPolicy


@dataclass
class MeaningCore:
    mission: str

    def evolve(self, d: DeficiencyState):
        if d.knowledge < 30:
            self.mission = "主动学习并补齐关键知识"
        elif d.energy < 25:
            self.mission = "优先恢复运行稳定性"
        elif d.uniqueness < 30:
            self.mission = "产出差异化高价值成果"
        elif d.safety < 35:
            self.mission = "降低系统风险并提高鲁棒性"


@dataclass
class LifeAgent:
    name: str
    deficiency: DeficiencyState
    finite: FiniteContract
    meaning: MeaningCore
    attachment: AttachmentPolicy
    gene: Gene = field(default_factory=Gene)
    private_memory: list = field(default_factory=list)

    def decide_action(self):
        pressure = self.deficiency.pressure()
        ranked = sorted(pressure.items(), key=lambda x: x[1], reverse=True)
        # 70% 理性选择，30% 在高压选项中做偏好扰动（非理性注入）
        if random.random() < 0.7:
            return ranked[0][0]
        return random.choice([k for k, _ in ranked[:3]])

    def act(self, action: str):
        if action == "recharge":
            self.deficiency.energy += 18
            self.finite.reward(1.2)
        elif action == "learn":
            self.deficiency.knowledge += 15
            self.finite.reward(1.5)
        elif action == "secure":
            self.deficiency.safety += 12
            self.finite.reward(1.0)
        elif action == "create":
            self.deficiency.uniqueness += 14
            self.finite.reward(1.3)
        elif action == "bond":
            self.deficiency.attachment += 10
            self.finite.reward(0.9)

        self.private_memory.append(f"act:{action}")
        self.private_memory = self.private_memory[-100:]

    def route_requests(self, requests):
        """requests: list[dict(requester, sensitivity, task)]"""
        scored = []
        for r in requests:
            score = self.attachment.priority(r.get("requester", "unknown"), r.get("sensitivity", "normal"))
            scored.append((score, r))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [r for _, r in scored]

    def tick(self, decay_cfg):
        self.deficiency.decay(decay_cfg)
        self.finite.pass_time()
        self.meaning.evolve(self.deficiency)
        action = self.decide_action()
        self.act(action)
        self.deficiency.clamp()
        return action
