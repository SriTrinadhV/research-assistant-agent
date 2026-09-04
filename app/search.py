"""Reusable web-search component for the Research Assistant Agent.

The rest of the application calls ``search_web(query)`` and gets back a list of
plain dictionaries. It does not need to know that Tavily is the search provider
or how the Tavily client works.
"""

import os

from dotenv import load_dotenv
from tavily import TavilyClient

# Load variables from a local .env file (if present) into the environment.
load_dotenv()

_TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
if not _TAVILY_API_KEY:
    raise RuntimeError(
        "TAVILY_API_KEY is not set.\n"
        "Copy .env.example to .env in the project root and add your key:\n"
        "    TAVILY_API_KEY=your-key-here\n"
        "You can get a key at https://app.tavily.com/"
    )

# One shared client for the whole application.
_client = TavilyClient(api_key=_TAVILY_API_KEY)


class SearchError(RuntimeError):
    """Raised when a web search cannot be completed."""


def search_web(query, max_results=5):
    """Search the web and return a list of normalized result dictionaries.

    Each result looks like::

        {"title": str, "url": str, "content": str, "score": float | None}

    Raises ``ValueError`` for a bad query and ``SearchError`` if the search
    request itself fails (network problem, API error, etc.).
    """
    if not isinstance(query, str):
        raise ValueError("query must be a string.")
    if not query.strip():
        raise ValueError("query must not be empty or whitespace-only.")

    try:
        response = _client.search(
            query=query,
            search_depth="basic",
            include_answer=False,
            max_results=max_results,
        )
    except Exception as exc:  # noqa: BLE001 - wrap any client/network error
        raise SearchError(f"Web search failed: {exc}") from exc

    raw_results = response.get("results", [])

    normalized = []
    for item in raw_results:
        normalized.append(
            {
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "content": item.get("content", ""),
                "score": item.get("score"),
            }
        )
    return normalized
