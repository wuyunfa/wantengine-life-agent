from dataclasses import dataclass, field
from .roles import PlannerAgent, ResearcherAgent, BuilderAgent, ReviewerAgent
from .memory_bus import SharedMemoryBus


@dataclass
class CollaborationOrchestrator:
    planner: PlannerAgent = field(default_factory=PlannerAgent)
    researcher: ResearcherAgent = field(default_factory=ResearcherAgent)
    builder: BuilderAgent = field(default_factory=BuilderAgent)
    reviewer: ReviewerAgent = field(default_factory=ReviewerAgent)
    bus: SharedMemoryBus = field(default_factory=SharedMemoryBus)

    def run_round(self, goal: str) -> dict:
        self.bus.put_fact("goal", goal, source="planner")

        plan = self.planner.run(goal)
        self.bus.put_fact("plan", plan, source="planner")

        self.bus.add_task({"name": "collect_context", "status": "open"})
        self.bus.add_task({"name": "propose_solution", "status": "open"})
        self.bus.add_task({"name": "implement_solution", "status": "open"})
        self.bus.add_task({"name": "review_and_refine", "status": "open"})

        claim_r = self.bus.claim_task("researcher")
        research = self.researcher.run(plan)
        if claim_r:
            self.bus.close_task(claim_r["name"], "context_collected", "researcher")
        self.bus.put_fact("research", research, source="researcher")

        claim_b = self.bus.claim_task("builder")
        build = self.builder.run(research)
        if claim_b:
            self.bus.close_task(claim_b["name"], "solution_built", "builder")
        self.bus.put_fact("build", build, source="builder")

        claim_v = self.bus.claim_task("reviewer")
        review = self.reviewer.run(build)
        if claim_v:
            self.bus.close_task(claim_v["name"], "review_done", "reviewer")
        self.bus.put_fact("review", review, source="reviewer")

        return {
            "goal": goal,
            "plan": plan,
            "research": research,
            "build": build,
            "review": review,
            "memory_bus": self.bus.snapshot(),
            "round_status": "done" if review["passed"] else "needs_refine",
        }
