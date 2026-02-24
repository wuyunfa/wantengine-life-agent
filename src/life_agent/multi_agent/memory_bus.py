from dataclasses import dataclass, field
from typing import Any


@dataclass
class SharedMemoryBus:
    """Simple blackboard for multi-agent collaboration (M2)."""

    facts: dict[str, Any] = field(default_factory=dict)
    tasks: list[dict[str, Any]] = field(default_factory=list)
    events: list[dict[str, Any]] = field(default_factory=list)

    def put_fact(self, key: str, value: Any, source: str = "system") -> None:
        self.facts[key] = value
        self.events.append({"type": "fact", "key": key, "source": source})

    def get_fact(self, key: str, default: Any = None) -> Any:
        return self.facts.get(key, default)

    def add_task(self, task: dict[str, Any]) -> None:
        self.tasks.append(task)
        self.events.append({"type": "task", "task": task.get("name", "unknown")})

    def claim_task(self, role: str) -> dict[str, Any] | None:
        for t in self.tasks:
            if t.get("status", "open") == "open":
                t["status"] = "claimed"
                t["owner"] = role
                self.events.append({"type": "claim", "role": role, "task": t.get("name", "unknown")})
                return t
        return None

    def close_task(self, task_name: str, result: str, role: str) -> bool:
        for t in self.tasks:
            if t.get("name") == task_name:
                t["status"] = "done"
                t["result"] = result
                t["owner"] = role
                self.events.append({"type": "close", "role": role, "task": task_name})
                return True
        return False

    def snapshot(self) -> dict[str, Any]:
        return {
            "facts": self.facts,
            "tasks": self.tasks,
            "events": self.events,
        }
