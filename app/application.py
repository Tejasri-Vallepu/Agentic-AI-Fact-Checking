from app.agents.orchestrator import FactCheckingOrchestrator
from app.agents.planner import PlannerAgent
from app.agents.researcher import ResearcherAgent
from app.agents.verifier import GeminiVerifier
from app.core.config import settings
from app.retrieval.embeddings import EmbeddingModel
from app.retrieval.retriever import EvidenceRetriever
from app.retrieval.vector_store import ChromaVectorStore


def create_application():
    embedding_model = EmbeddingModel()

    vector_store = ChromaVectorStore(
        settings.vector_db_path
    )

    retriever = EvidenceRetriever(
        embedding_model=embedding_model,
        vector_store=vector_store,
    )

    planner = PlannerAgent()
    researcher = ResearcherAgent(retriever)
    verifier = GeminiVerifier()

    return FactCheckingOrchestrator(
        planner=planner,
        researcher=researcher,
        verifier=verifier,
    )
