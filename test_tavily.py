"""Minimal Tavily Search connectivity test.

Runs a single basic web search and prints the results. This is only a
connectivity check for Step 2 of the Research Assistant Agent project --
no AI answer generation, no source extraction, no synthesis.
"""

import sys

from dotenv import load_dotenv
import os

from tavily import TavilyClient

TEST_QUERY = "What are the latest developments in solid-state batteries?"


def main() -> int:
    load_dotenv()

    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        print(
            "ERROR: TAVILY_API_KEY is not set.\n"
            "Create a .env file at the project root (copy .env.example) and add:\n"
            "    TAVILY_API_KEY=your-key-here\n"
            "You can get a key at https://app.tavily.com/",
            file=sys.stderr,
        )
        return 1

    client = TavilyClient(api_key=api_key)

    try:
        response = client.search(
            query=TEST_QUERY,
            search_depth="basic",
            include_answer=False,
            max_results=3,
        )
    except Exception as exc:  # noqa: BLE001 - surface any client/API error clearly
        print(f"ERROR: Tavily search failed: {exc}", file=sys.stderr)
        return 1

    results = response.get("results", [])
    print(f'Query: "{TEST_QUERY}"')
    print(f"Results returned: {len(results)}\n")

    if not results:
        print("No results returned.")
        return 0

    for i, result in enumerate(results, start=1):
        title = result.get("title", "(no title)")
        url = result.get("url", "(no url)")
        content = result.get("content", "").strip()
        score = result.get("score")

        print(f"[{i}] {title}")
        print(f"    URL: {url}")
        if score is not None:
            print(f"    Relevance score: {score}")
        print(f"    Snippet: {content}")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
