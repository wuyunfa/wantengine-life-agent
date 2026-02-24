from dataclasses import dataclass


@dataclass
class PlannerAgent:
    name: str = "planner"

    def run(self, goal: str) -> dict:
        return {
            "goal": goal,
            "tasks": [
                "collect_context",
                "propose_solution",
                "implement_solution",
                "review_and_refine",
            ],
            "acceptance": ["runnable", "documented", "tested"],
        }


@dataclass
class ResearcherAgent:
    name: str = "researcher"

    def run(self, plan: dict) -> dict:
        evidence = {
            "key_constraints": [
                "keep module boundaries clear",
                "prioritize runnable output",
                "preserve reproducibility",
            ],
            "design_notes": [
                "separate policy from execution",
                "log every round for traceability",
            ],
        }
        return {"plan": plan, "evidence": evidence}


@dataclass
class BuilderAgent:
    name: str = "builder"

    def run(self, research_pack: dict) -> dict:
        implementation = {
            "status": "implemented",
            "artifacts": [
                "coordinator_logic",
                "structured_round_report",
                "handoff_contract",
            ],
            "notes": "minimal viable implementation completed",
        }
        return {"research_pack": research_pack, "implementation": implementation}


@dataclass
class ReviewerAgent:
    name: str = "reviewer"

    def run(self, build_pack: dict) -> dict:
        impl = build_pack["implementation"]
        passed = impl.get("status") == "implemented" and len(impl.get("artifacts", [])) >= 3
        return {
            "passed": passed,
            "checks": {
                "runnable": True,
                "documented": True,
                "tested": passed,
            },
            "next_actions": [] if passed else ["add_missing_tests"],
        }
