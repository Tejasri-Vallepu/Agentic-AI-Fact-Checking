from app.application import create_application
from app.core.config import settings
from app.data.loader import DatasetLoader


def main():
    loader = DatasetLoader(settings.project_root)
    claim = loader.load_split("train")[0]

    system = create_application()

    evidence = system.researcher.research(
        claim.claim_text,
        top_k=5,
    )

    print("\nClaim:")
    print(claim.claim_text)

    print("\nRetrieved evidence:")

    for item in evidence:
        print(
            f"\nID: {item['document_id']}"
            f"\nScore: {item['score']:.4f}"
            f"\nText: {item['text'][:500]}"
        )


if __name__ == "__main__":
    main()
