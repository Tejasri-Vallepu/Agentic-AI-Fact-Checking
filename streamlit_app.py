import streamlit as st


st.set_page_config(
    page_title="Agentic Fact Checker",
    page_icon="🔎",
    layout="wide",
)


@st.cache_resource
def get_system():
    from app.application import create_application
    return create_application()


st.title("🔎 Agentic Fact Checking System")
st.caption(
    "Planner Agent → Researcher Agent → ChromaDB Evidence → Gemini Verifier"
)

claim = st.text_area(
    "Enter a factual claim",
    placeholder="Example: The Earth revolves around the Sun.",
    height=120,
)

top_k = st.slider(
    "Number of evidence documents",
    min_value=1,
    max_value=10,
    value=5,
)


if st.button("Verify Claim", type="primary"):
    if not claim.strip():
        st.warning("Please enter a claim.")
        st.stop()

    try:
        with st.spinner("Running agentic fact-checking workflow..."):
            output = get_system().run(
                claim_text=claim.strip(),
                top_k=top_k,
            )

        result = output["result"]

        st.subheader("Final Verdict")
        st.metric(
            "Verdict",
            result.verdict,
            f"Confidence: {result.confidence:.2%}",
        )

        st.subheader("Explanation")
        st.write(result.explanation)

        st.subheader("Reasoning Summary")
        st.write(result.reasoning_summary)

        if result.key_facts:
            st.subheader("Key Facts")
            for fact in result.key_facts:
                st.write(f"• {fact}")

        st.subheader("Agent Workflow")
        for step in output["plan"]:
            st.write(f"→ {step}")

        st.subheader("Retrieved Evidence")

        for index, item in enumerate(output["evidence"], start=1):
            with st.expander(
                f"{index}. {item['document_id']} | score={item['score']:.4f}"
            ):
                st.write(item["text"])

    except Exception as exc:
        st.error(f"Fact-checking failed: {exc}")
        st.info(
            "Make sure .env contains GEMINI_API_KEY and that "
            "scripts\\build_vector_db.py has been executed."
        )
