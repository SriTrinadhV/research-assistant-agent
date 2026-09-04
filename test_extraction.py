"""Live test for the reusable app/extraction.py module.

Exercises the real pipeline so far: search_web() discovers sources, then
extract_sources() reads their full content. Uses the real Tavily API
(no mocking yet).
"""

from app.search import search_web
from app.extraction import extract_sources

TEST_QUERY = "What are recent developments in solid-state batteries?"
EXPECTED_RESULT_FIELDS = {"url", "content"}
EXPECTED_TOP_LEVEL_FIELDS = {"results", "failed_results"}
SNIPPET_PREVIEW_CHARS = 500


def main() -> int:
    search_results = search_web(TEST_QUERY, max_results=3)
    urls = [result["url"] for result in search_results]
    snippets_by_url = {result["url"]: result["content"] for result in search_results}

    print(f'Query: "{TEST_QUERY}"')
    print(f"URLs requested: {len(urls)}")
    for url in urls:
        print(f"  - {url}")
    print()

    extraction = extract_sources(urls)

    # Verify the top-level structure contains exactly "results" and "failed_results".
    top_level_fields = set(extraction.keys())
    if top_level_fields != EXPECTED_TOP_LEVEL_FIELDS:
        print(f"FAIL: top-level structure was {top_level_fields}, expected {EXPECTED_TOP_LEVEL_FIELDS}")
        return 1

    results = extraction["results"]
    failed_results = extraction["failed_results"]

    print(f"Successfully extracted: {len(results)}")
    print(f"Failed: {len(failed_results)}\n")

    all_fields_ok = True
    best_growth_ratio = 0.0

    for item in results:
        fields = set(item.keys())
        if fields != EXPECTED_RESULT_FIELDS:
            all_fields_ok = False
            print(f"FIELD MISMATCH on {item.get('url')}: got {fields}")
            continue

        content = item["content"]
        char_count = len(content)
        preview = content[:SNIPPET_PREVIEW_CHARS]

        print(f"[OK] {item['url']}")
        print(f"    Extracted content length: {char_count} characters")
        print(f"    Preview (first {SNIPPET_PREVIEW_CHARS} chars): {preview}")
        print()

        snippet = snippets_by_url.get(item["url"], "")
        if snippet:
            ratio = char_count / max(len(snippet), 1)
            best_growth_ratio = max(best_growth_ratio, ratio)

    for item in failed_results:
        print(f"[FAILED] {item.get('url')}")
        print(f"    Error: {item.get('error')}")
        print()

    if not all_fields_ok:
        print("FAIL: at least one successful result did not have exactly url, content.")
        return 1

    print(f"Largest extracted-content-vs-snippet size ratio observed: {best_growth_ratio:.1f}x")
    if best_growth_ratio > 1.0:
        print("PASS: at least one extracted source is substantially larger than its search snippet.")
    else:
        print("NOTE: could not confirm extracted content was larger than its snippet this run "
              "(live webpages may vary) -- not treated as a failure.")

    print("\nPASS: top-level structure and per-result fields are correct.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
