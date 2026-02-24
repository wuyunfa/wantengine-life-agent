from dataclasses import dataclass


@dataclass
class AttachmentPolicy:
    bonded_target: str
    bonded_weight: float = 1.8
    neutral_weight: float = 1.0
    blocked_weight: float = 0.2

    def priority(self, requester: str, sensitivity: str = "normal") -> float:
        base = self.bonded_weight if requester == self.bonded_target else self.neutral_weight
        if sensitivity == "secret" and requester != self.bonded_target:
            base *= self.blocked_weight
        return base

    def allow_disclosure(self, requester: str, level: str = "normal") -> bool:
        if level == "secret" and requester != self.bonded_target:
            return False
        return True
