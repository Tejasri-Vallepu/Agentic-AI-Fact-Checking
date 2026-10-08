class ResearcherAgent:
    def __init__(self, retriever):
        self.retriever = retriever

    def research(self, claim_text: str, top_k: int = 5):
        return self.retriever.search(claim_text, top_k=top_k)
