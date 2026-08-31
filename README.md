# Research Assistant Agent

A beginner AI project. This project will take a user's research question and
produce an answer by:

1. Searching the web for relevant information.
2. Extracting content from the discovered sources.
3. Synthesizing a response using a Gemini model.

## Status

Initial project setup only. No application logic has been implemented yet.

## Setup

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env  # then fill in your API keys
```

## Environment variables

See `.env.example`:

- `GEMINI_API_KEY` - API key for Gemini.
- `TAVILY_API_KEY` - API key for the Tavily web search API.
