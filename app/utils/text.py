from collections import Counter
import math
import re

TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9_]+")


def tokenize(value: str) -> list[str]:
    return [token.lower() for token in TOKEN_PATTERN.findall(value)]


def cosine_similarity(a: Counter[str], b: Counter[str]) -> float:
    common = set(a) & set(b)
    numerator = sum(a[token] * b[token] for token in common)
    norm_a = math.sqrt(sum(count * count for count in a.values()))
    norm_b = math.sqrt(sum(count * count for count in b.values()))
    if not norm_a or not norm_b:
        return 0.0
    return numerator / (norm_a * norm_b)
