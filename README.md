# 🤖 Agentic Fact-Checking System

An **Agentic AI-powered fact-checking system** that verifies factual claims using **semantic evidence retrieval, ChromaDB, and Google Gemini**.

The system follows an evidence-first workflow where relevant documents are retrieved before Gemini makes the final verification decision.

---

## 🚀 Project Overview

Given a factual claim, the system:

1. Creates a verification plan using a **Planner Agent**
2. Retrieves relevant evidence using **Sentence Transformers**
3. Searches the evidence using **ChromaDB**
4. Passes the retrieved evidence to **Gemini**
5. Generates an evidence-grounded verdict
6. Returns the verdict with **confidence, explanation, reasoning, and evidence IDs**

### Example Workflow

```text
User Claim
    ↓
Planner Agent
    ↓
Researcher Agent
    ↓
Sentence Transformer Embeddings
    ↓
ChromaDB Semantic Retrieval
    ↓
Relevant Evidence
    ↓
Gemini Verifier
    ↓
Structured Fact-Check Result

🎯 Key Features
-Agentic workflow with Planner, Researcher, and Verifier agents
-Semantic evidence retrieval using Sentence Transformers
-Vector search using ChromaDB
-Evidence-grounded verification using Google Gemini
-Structured LLM outputs using Pydantic
-Confidence score and reasoning summary
-Retrieval evaluation using Recall@K
-Streamlit interface for interactive demonstration
-FastAPI backend for API-based integration
-Modular architecture designed for future production upgrades

##Architecture:

                         ┌─────────────────┐
                         │   User Claim    │
                         └────────┬────────┘
                                  ↓
                         ┌─────────────────┐
                         │  Planner Agent  │
                         └────────┬────────┘
                                  ↓
                         ┌─────────────────┐
                         │ Researcher Agent│
                         └────────┬────────┘
                                  ↓
                  ┌────────────────────────────┐
                  │ Semantic Evidence Retrieval│
                  └─────────────┬──────────────┘
                                ↓
                    ┌─────────────────────┐
                    │ Sentence Transformer│
                    └──────────┬──────────┘
                               ↓
                       ┌──────────────┐
                       │   ChromaDB   │
                       └──────┬───────┘
                              ↓
                       Retrieved Evidence
                              ↓
                     ┌─────────────────┐
                     │  Gemini Verifier│
                     └────────┬────────┘
                              ↓
                    ┌────────────────────┐
                    │ Structured Result  │
                    │ Verdict            │
                    │ Confidence         │
                    │ Explanation        │
                    │ Evidence IDs       │
                    └────────────────────┘
					
## Tech Stack:
					
| Category           | Technology                      |
| ------------------ | ------------------------------- |
| Language           | Python                          |
| LLM                | Google Gemini                   |
| Agent Architecture | Planner + Researcher + Verifier |
| Embeddings         | Sentence Transformers           |
| Vector Database    | ChromaDB                        |
| Data Processing    | Pandas, NumPy                   |
| Validation         | Pydantic                        |
| API                | FastAPI                         |
| UI                 | Streamlit                       |
| Testing            | Pytest                          |
| Logging            | Loguru                          |
| ML Utilities       | Scikit-learn                    |

📂 Project Structure
Agentic Fact Checking Project/
│
├── app/
│   ├── agents/
│   │   ├── planner.py
│   │   ├── researcher.py
│   │   ├── verifier.py
│   │   └── orchestrator.py
│   │
│   ├── retrieval/
│   │   ├── embeddings.py
│   │   ├── document_loader.py
│   │   ├── vector_store.py
│   │   └── retriever.py
│   │
│   ├── schemas/
│   │   ├── claim.py
│   │   └── fact_check.py
│   │
│   ├── preprocessing/
│   ├── data/
│   ├── evaluation/
│   ├── llm/
│   ├── api/
│   └── core/
│
├── scripts/
│   ├── build_vector_db.py
│   └── evaluate_retrieval.py
│
├── tests/
│
├── streamlit_app.py
├── main.py
├── test_gemini.py
├── test_part2.py
├── test_retrieval.py
└── requirements.txt

🔍 How It Works
1. Claim Processing

The user enters a factual claim.

Example:

The claim is passed to the fact-checking system.

The claim is normalized and converted into a structured Pydantic object.

2. Planning

The Planner Agent creates the verification workflow:

Retrieve Evidence
        ↓
Compare Evidence
        ↓
Verify with Gemini
3. Evidence Retrieval

The claim is converted into an embedding using:

all-MiniLM-L6-v2

ChromaDB then retrieves the most semantically relevant evidence documents.

4. Gemini Verification

Gemini receives:

Claim
+
Retrieved Evidence

The model is instructed to make the decision only from the supplied evidence.

5. Structured Output

The final response follows a Pydantic schema:

Verdict
Confidence
Explanation
Key Facts
Evidence IDs
Reasoning Summary

Possible verdicts:

SUPPORTED
REFUTED
PARTIALLY_SUPPORTED
INSUFFICIENT_EVIDENCE


📊 Evaluation

The project includes retrieval evaluation using:

Recall@1
Recall@3
Recall@5

💻 Demo

The system provides an interactive Streamlit application.

Run:

streamlit run streamlit_app.py


📈 Future Improvements

The architecture can be extended with:

Hybrid BM25 + Dense Retrieval
Cross-Encoder Reranking
Web Search Agent
External Article Retrieval
Citation Verification
Multi-Agent Debate
Multilingual Fact Checking
Confidence Calibration
Observability and Tracing
Docker-based Deployment
Cloud Vector Database

👨‍💻 Skills Demonstrated

This project demonstrates practical experience in:

Python • Generative AI • Agentic AI • LLMs • RAG • Semantic Search • Vector Databases • Prompt Engineering • Structured LLM Outputs • API Development • Streamlit • Evaluation • Modular Software Architecture

