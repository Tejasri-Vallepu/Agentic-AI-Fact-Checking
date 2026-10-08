from app.llm import gemini_client


def main():
    prompt = """
You are an AI fact-checking assistant.
Explain in two sentences how evidence helps
verify a factual claim.
"""

    response = gemini_client.generate(prompt)

    print("\nGemini response:")
    print(response)


if __name__ == "__main__":
    main()
