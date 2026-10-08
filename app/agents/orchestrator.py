class FactCheckingOrchestrator:
    def __init__(self, planner, researcher, verifier):
        self.planner = planner
        self.researcher = researcher
        self.verifier = verifier

    def run(self, claim_text: str, top_k: int = 5):
        plan = self.planner.create_plan(claim_text)

        evidence = self.researcher.research(
            claim_text,
            top_k=top_k,
        )

        result = self.verifier.verify(
            claim_text,
            evidence,
        )

        return {
            "claim": claim_text,
            "plan": plan,
            "evidence": evidence,
            "result": result,
        }
