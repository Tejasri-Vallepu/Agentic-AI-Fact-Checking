import re
import unicodedata


def normalize_unicode(text: str) -> str:
    if not text:
        return ""
    return unicodedata.normalize("NFKC", text)


def clean_text(text: str) -> str:
    if not text:
        return ""

    text = normalize_unicode(text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def normalize_claim(claim: str) -> str:
    claim = clean_text(claim)
    return claim.strip("\"' ")
