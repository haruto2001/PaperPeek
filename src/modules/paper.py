import logging
import urllib.parse
from dataclasses import dataclass
from typing import Optional

import feedparser


@dataclass(frozen=True)
class Paper:
    """
    A class representing a paper with a title and summary.

    Attributes:
        title (str): The title of the paper.
        summary (str): A brief summary of the paper.
    """

    title: str
    summary: str


class ArxivPaperFetcher:
    """
    A class to fetch papers from the arXiv API based on a search query.

    Attributes:
        BASE_URL (str): The base URL of the arXiv API.
        logger (logging.Logger): Logger instance for logging events.
        cache (dict[str, list[Paper]]): A dictionary to cache query results and reduce redundant API calls.

    Methods:
        fetch_papers(search_query: str, max_results: int, sort_by: str, sort_order: str) -> list[Paper]:
            Fetches papers from the arXiv API based on the provided query parameters.

        clear_cache() -> None:
            Clears the internal cache of previously fetched papers.
    """

    BASE_URL = "http://export.arxiv.org/api/query"

    def __init__(self, logger: logging.Logger) -> None:
        """
        Initializes the ArxivPaperFetcher instance with an empty cache.

        Args:
            logger (logging.Logger): Logger instance for logging events.
        """
        self.logger = logger
        self.cache = {}

    def fetch_papers(
        self, search_query: str, max_results: int, sort_by: str = "submittedDate", sort_order: str = "descending"
    ) -> list[Paper]:
        """
        Fetches a list of papers from the arXiv API based on the search query and parameters.

        Caches the result of each query to avoid redundant API calls.

        Args:
            search_query (str): The query string to search for in the arXiv papers.
            max_results (int): The maximum number of results to fetch.
            sort_by (Optional[str]): The field to sort the results by (e.g., "relevance", "lastUpdatedDate", or "submittedDate").
            sort_order (Optional[str]): The order to sort the results in ("ascending" or "descending").

        Returns:
            list[Paper]: A list of Paper objects containing the title and summary of each fetched paper.
        """
        cache_key = f"{search_query}_{max_results}_{sort_by}_{sort_order}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        query_params = {
            "search_query": f"all:{search_query}",
            "start": 0,
            "max_results": max_results,
            # "sortBy": sort_by,
            # "sortOrder": sort_order,
        }
        url = self.BASE_URL + "?" + urllib.parse.urlencode(query_params)

        self.logger.info(f"Fetching papers from URL: {url}")
        feed = feedparser.parse(url)
        if feed.bozo:
            self.logger.error(f"Error parsing feed: (stasus={feed.status})")

        breakpoint()
        papers = []
        for entry in feed.entries:
            paper = Paper(title=entry.title, summary=entry.summary)
            papers.append(paper)

        self.cache[cache_key] = papers

        return papers

    def clear_cache(self) -> None:
        """
        Clears the internal cache of previously fetched papers.
        """
        self.cache.clear()


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s %(filename)s %(funcName)s():%(lineno)s\n"
        "[%(levelname)s] %(message)s\n"
    )

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    fetcher = ArxivPaperFetcher(logger)
    search_query = "electron"
    max_results = 10
    papers = fetcher.fetch_papers(search_query=search_query, max_results=max_results)
    print(papers)

