import random
import re
from dataclasses import dataclass, field


@dataclass
class TaskGenerator:
    max_history: int = 8
    exploration_chance: float = 0.2
    execution_history: list[str] = field(default_factory=list)

    domain_library: dict = field(default_factory=lambda: {
        "tech": {
            "hobby": ["AI", "robotics", "python"],
            "skill": ["automation scripting", "version control", "model calling"],
            "knowledge": ["AI architecture", "control theory", "open-source workflow"],
            "content": ["coding tutorials", "project guides", "technology updates"],
        },
        "media": {
            "hobby": ["photography", "video editing", "music"],
            "skill": ["editing methods", "color grading", "recording methods"],
            "knowledge": ["audio-visual language", "music theory", "equipment knowledge"],
            "content": ["shooting tutorials", "editing guides", "work appreciation"],
        },
    })

    general_vocab: dict = field(default_factory=lambda: {
        "platform": ["GitHub", "YouTube", "Medium", "InfoQ"],
        "media_type": ["article", "video", "podcast"],
        "content_type": ["tutorial", "guide", "review"],
        "learning_material": ["beginner tutorials", "systematic courses"],
        "tool": ["Python", "VS Code", "Excel"],
        "plan_target": ["interest learning plan", "weekly to-do"],
        "resource": ["tutorial resources", "inspiration references"],
        "project": ["small works", "automation tools"],
        "project_type": ["personal blog", "portfolio website"],
        "topic": ["personal growth", "creative inspiration"],
        "creation": ["articles", "videos", "notes"],
    })

    boredom_actions: list[str] = field(default_factory=lambda: [
        "organize", "backup", "summarize", "review", "update", "optimize"
    ])
    boredom_targets: list[str] = field(default_factory=lambda: [
        "desktop files", "PDF documents", "work documents", "learning notes"
    ])
    plan_type: list[str] = field(default_factory=lambda: [
        "weekend leisure", "weekly to-do", "monthly reading", "fitness schedule"
    ])
    life_target: list[str] = field(default_factory=lambda: [
        "reading list", "travel destination list", "shopping list", "learning plan"
    ])

    boredom_tasks: list[dict] = field(default_factory=lambda: [
        {"template": "I'm a bit bored and want to {action} my {target}", "complexity": "simple"},
        {"template": "I have nothing to do, so I'll check out popular {content_type} in {hobby}", "complexity": "simple"},
        {"template": "With nothing to do, I'll make a simple list for my {plan_type}", "complexity": "simple"},
        {"template": "I'll update my {project} related to {hobby}", "complexity": "medium"},
    ])

    curiosity_tasks: list[dict] = field(default_factory=lambda: [
        {"template": "I want to learn about {content} in the {hobby} field", "complexity": "complex"},
        {"template": "I want to deeply learn the {skill} related to {hobby}", "complexity": "complex"},
        {"template": "I'll research core {knowledge} in the {hobby} field", "complexity": "complex"},
    ])

    exploration_template: dict = field(default_factory=lambda: {
        "simple": [
            "I want to explore {hobby}-related {content_type}",
            "I want to organize my {target}",
        ],
        "medium": [
            "I want to learn a simple {skill} via {learning_material}",
            "I want to plan my {plan_target}",
        ],
        "complex": [
            "I want to build a {project_type} for {hobby}",
            "I want to organize a complete knowledge base about {hobby}",
        ],
    })

    @staticmethod
    def _pick(arr: list[str], default: str) -> str:
        return random.choice(arr) if arr else default

    def _domain(self) -> tuple[str, dict]:
        key = random.choice(list(self.domain_library.keys()))
        return key, self.domain_library[key]

    def _render(self, template: str, domain: dict) -> str:
        variables = re.findall(r"\{(\w+)\}", template)
        out = template
        hobby = self._pick(domain.get("hobby", []), "learning")
        for var in variables:
            if var == "hobby":
                val = hobby
            elif var in domain:
                val = self._pick(domain[var], "content")
            elif var in self.general_vocab:
                val = self._pick(self.general_vocab[var], "content")
            elif var == "action":
                val = self._pick(self.boredom_actions, "organize")
            elif var == "target":
                val = self._pick(self.boredom_targets, "files")
            elif var == "plan_type":
                val = self._pick(self.plan_type, "weekly to-do")
            elif var == "life_target":
                val = self._pick(self.life_target, "reading list")
            else:
                val = "content"
            out = out.replace(f"{{{var}}}", val)
        return out

    def _dedupe(self, task: str) -> str:
        if task in self.execution_history:
            task = task + " (variant)"
        self.execution_history.append(task)
        self.execution_history = self.execution_history[-self.max_history:]
        return task

    def generate(self, task_type: str) -> tuple[str, str]:
        if random.random() < self.exploration_chance:
            complexity = random.choice(["simple", "medium", "complex"])
            tpl = self._pick(self.exploration_template[complexity], "I want to explore {hobby}")
            _, domain = self._domain()
            task = self._render(tpl, domain)
            return self._dedupe(task), complexity

        if task_type == "curiosity":
            data = random.choice(self.curiosity_tasks)
        else:
            data = random.choice(self.boredom_tasks)

        _, domain = self._domain()
        task = self._render(data["template"], domain)
        return self._dedupe(task), data["complexity"]
