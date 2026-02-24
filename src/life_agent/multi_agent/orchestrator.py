from dataclasses import dataclass, field
from .roles import PlannerAgent, ResearcherAgent, BuilderAgent, ReviewerAgent


@dataclass
class CollaborationOrchestrator:
    planner: PlannerAgent = field(default_factory=PlannerAgent)
    researcher: ResearcherAgent = field(default_factory=ResearcherAgent)
    builder: BuilderAgent = field(default_factory=BuilderAgent)
    reviewer: ReviewerAgent = field(default_factory=ReviewerAgent)

    def run_round(self, goal: str) -> dict:
        plan = self.planner.run(goal)
        research = self.researcher.run(plan)
        build = self.builder.run(research)
        review = self.reviewer.run(build)

        return {
            "goal": goal,
            "plan": plan,
            "research": research,
            "build": build,
            "review": review,
            "round_status": "done" if review["passed"] else "needs_refine",
        }
