class PlannerAgent:
    """
    Creates the verification plan.

    This first version is deterministic so the workflow is predictable.
    Later, the planner can become an LLM/tool-using agent.
    """

    def create_plan(self, claim_text: str) -> list[str]:
        return [
            "retrieve_local_evidence",
            "compare_claim_with_evidence",
            "verify_claim_with_gemini",
        ]
