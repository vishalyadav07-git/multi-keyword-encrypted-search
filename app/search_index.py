import os
import re
import hmac
import hashlib
from collections import Counter

from dotenv import load_dotenv

load_dotenv()

SEARCH_KEY = os.getenv("SEARCH_KEY")

STOP_WORDS = {
    "a",
    "an",
    "the",
    "is",
    "am",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "and",
    "or",
    "for",
    "to",
    "of",
    "in",
    "on",
    "at",
    "with",
    "by"
}


def extract_keywords(text: str):

    words = re.findall(
        r"\b[a-zA-Z0-9]+\b",
        text.lower()
    )

    return [
        word
        for word in words
        if word not in STOP_WORDS
    ]


def hash_keyword(keyword: str) -> str:

    return hmac.new(
        SEARCH_KEY.encode(),
        keyword.encode(),
        hashlib.sha256
    ).hexdigest()


def create_keyword_index(text: str):

    words = extract_keywords(text)

    word_count = Counter(words)

    keyword_index = []

    for keyword, frequency in word_count.items():

        keyword_hash = hash_keyword(keyword)

        keyword_index.append({
            "keyword_hash": keyword_hash,
            "frequency": frequency
        })

    return keyword_index

