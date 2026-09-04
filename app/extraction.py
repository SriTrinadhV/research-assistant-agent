"""Reusable source-content extraction component for the Research Assistant Agent.

The rest of the application calls ``extract_sources(urls)`` and gets back the
actual webpage content for those URLs. It does not need to know that Tavily
Extract is the provider or how the Tavily client works.
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

_MAX_URLS = 20


class ExtractionError(RuntimeError):
    """Raised when source content cannot be extracted."""


def _normalize_urls(urls):
    """Validate input and return a clean list of URL strings."""
    if isinstance(urls, str):
        urls = [urls]

    if not isinstance(urls, list):
        raise ValueError("urls must be a string or a list of strings.")

    if not urls:
        raise ValueError("urls must not be empty.")

    if len(urls) > _MAX_URLS:
        raise ValueError(f"Too many URLs: got {len(urls)}, max is {_MAX_URLS}.")

    for url in urls:
        if not isinstance(url, str):
            raise ValueError(f"Each URL must be a string, got: {url!r}")
        if not url.strip():
            raise ValueError("URLs must not be empty or whitespace-only.")

    return urls


def extract_sources(urls):
    """Extract webpage content for one or more URLs.

    ``urls`` may be a single URL string or a list of URL strings.

    Returns a dict::

        {
            "results": [{"url": str, "content": str}, ...],
            "failed_results": [{"url": str, "error": str}, ...],
        }

    Raises ``ValueError`` for bad input and ``ExtractionError`` if the
    extraction request itself fails (network problem, API error, etc.).
    """
    url_list = _normalize_urls(urls)

    try:
        response = _client.extract(
            urls=url_list,
            extract_depth="basic",
            include_images=False,
        )
    except Exception as exc:  # noqa: BLE001 - wrap any client/network error
        raise ExtractionError(f"Source extraction failed: {exc}") from exc

    raw_results = response.get("results", [])
    raw_failed = response.get("failed_results", [])

    results = []
    for item in raw_results:
        results.append(
            {
                "url": item.get("url", ""),
                "content": item.get("raw_content", "") or "",
            }
        )

    failed_results = []
    for item in raw_failed:
        failed_results.append(
            {
                "url": item.get("url", ""),
                "error": item.get("error", "Unknown extraction error"),
            }
        )

    return {"results": results, "failed_results": failed_results}
