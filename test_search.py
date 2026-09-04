"""Live test for the reusable app/search.py module.

Uses the real Tavily API (no mocking yet).
"""

from app.search import search_web

TEST_QUERY = "What are recent developments in solid-state batteries?"
EXPECTED_FIELDS = {"title", "url", "content", "score"}


def main() -> int:
    results = search_web(TEST_QUERY, max_results=3)

    print(f'Query: "{TEST_QUERY}"')
    print(f"Number of results: {len(results)}\n")

    all_ok = True
    for i, result in enumerate(results, start=1):
        print(f"[{i}] {result['title']}")
        print(f"    URL: {result['url']}")
        print(f"    Score: {result['score']}")
        print(f"    Snippet: {result['content']}")

        fields = set(result.keys())
        if fields == EXPECTED_FIELDS:
            print("    Fields: OK (title, url, content, score)")
        else:
            all_ok = False
            missing = EXPECTED_FIELDS - fields
            extra = fields - EXPECTED_FIELDS
            print(f"    Fields: MISMATCH  missing={missing or '{}'} extra={extra or '{}'}")
        print()

    if not all_ok:
        print("FAIL: at least one result did not have exactly the expected fields.")
        return 1

    print("PASS: every result has exactly title, url, content, score.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
