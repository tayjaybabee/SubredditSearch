from dataclasses import dataclass
from typing import List, Dict
from subreddit_search.search import search_subreddits


@dataclass(frozen=True)
class Subreddit:
    name: str
    rank: str
    listing_stat: str
    url: str
    filter_type: str


class SubredditManager:
    def __init__(self):
        self.subreddits: Dict[str, Subreddit] = {}

    def add_subreddit(self, subreddit: Subreddit):
        self.subreddits[subreddit.name] = subreddit

    def get_subreddit(self, name: str) -> Subreddit:
        return self.subreddits.get(name, None)

    def get_all_subreddits(self) -> List[Subreddit]:
        return list(self.subreddits.values())

    @property
    def name_list(self) -> List[str]:
        return self.get_all_names()

    def get_all_names(self) -> List[str]:
        return list(self.subreddits.keys())

    def search(self, query: str, threshold: int = 80) -> List[str]:
        return search_subreddits(query, self.get_all_names(), threshold)
