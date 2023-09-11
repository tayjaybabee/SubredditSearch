import requests
from bs4 import BeautifulSoup
from subreddit_search.cache_management import CacheManager
from subreddit_search.app import App
import time


class SubredditScraper(App):
    def __init__(self, url, cache_expiry=3600, cache_dir=None):
        self.url = url
        self.cache_expiry = cache_expiry

        if cache_dir is None:
            self.cache_dir = self.PATHS.cache_dir
        else:
            self.cache_dir = cache_dir

        self.cache_manager = CacheManager(self.cache_dir, self.cache_expiry)
        self.cache_path = self.cache_manager.generate_cache_path(self.url)

        if self.cache_manager.is_cache_valid(self.cache_path):
            self.html_content = self.cache_manager.load_from_cache(self.cache_path)
        else:
            self._fetch_url_content()
            self.cache_manager.update_cache(self.cache_path, self.html_content)

        self.soup = BeautifulSoup(self.html_content, 'html.parser')

    def _fetch_url_content(self):
        res = requests.get(self.url)
        if res.status_code == 200:
            self.html_content = res.text
        else:
            raise Exception("Failed to fetch the URL")

    def extract_subreddits(self) -> dict:
        subreddit_info = {}
        for div in self.soup.find_all('div', {'class': 'listing-item'}):
            subreddit_name = div.get('data-target-subreddit', '')
            filter_type = div.get('data-target-filter', '')
            rank = div.find('span', {'class': 'rank-value'}).text if div.find('span', {'class': 'rank-value'}) else ''
            listing_stat = div.find('span', {'class': 'listing-stat'}).text if div.find('span', {
                'class': 'listing-stat'}) else ''
            url = div.find('a', {'class': filter_type})['href'] if div.find('a', {'class': filter_type}) else ''

            subreddit_info[subreddit_name] = {
                'rank': rank,
                'listing_stat': listing_stat,
                'url': url,
                'filter': filter_type
            }
        return subreddit_info

    def get_total_pages(self, base_url: str, sleep_time: float = 1.0, max_pages: int = None) -> int:
        """
        Determine the total number of pages available with rate limiting.

        Args:
            base_url (str): The base URL for the pages (e.g., "https://redditlist.com/sfw").
            sleep_time (float): Time to sleep between requests in seconds. Default is 1 second.
            max_pages (int, optional): Maximum number of pages to check.

        Returns:
            int: The total number of pages.
        """
        page_number = 1
        while True:
            if max_pages and page_number > max_pages:
                return max_pages

            url = f"{base_url}{page_number}.html" if page_number > 1 else f"{base_url}.html"
            res = requests.get(url)

            # Stop if the status code indicates that the page was not found
            if res.status_code == 404:
                return page_number - 1

            # Otherwise, proceed to the next page
            page_number += 1

            # Sleep to rate-limit the requests
            time.sleep(sleep_time)
