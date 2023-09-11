from rapidfuzz import fuzz, process
from typing import List, Dict


def search_subreddits(query: str, data: List[str], threshold: int = 80) -> List[str]:
    results = process.extract(query, data, limit=None, score_cutoff=threshold)
    return [match[0] for match in results]


