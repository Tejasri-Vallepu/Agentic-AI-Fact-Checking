from app.core.config import settings
from app.data.loader import DatasetLoader


def main():
    loader = DatasetLoader(settings.project_root)

    train = loader.load_split("train")

    print(f"Train claims loaded: {len(train)}")

    for index, claim in enumerate(train[:3], start=1):
        print(f"\n--- Claim {index} ---")
        print("ID:", claim.claim_id)
        print("Claim:", claim.claim_text)
        print("Label:", claim.label)
        print("Premise articles:", claim.premise_articles)
        print("Review article:", claim.review_article)


if __name__ == "__main__":
    main()
