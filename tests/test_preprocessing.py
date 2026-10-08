from app.preprocessing.text import clean_text, normalize_claim


def test_clean_text():
    assert clean_text("  hello   world  ") == "hello world"


def test_normalize_claim():
    assert normalize_claim('"Hello world"') == "Hello world"
