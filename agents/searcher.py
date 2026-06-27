import os
import requests
from dotenv import load_dotenv

load_dotenv()

def _search_tavily(claim: str) -> list:
    """Search using Tavily API."""
    try:
        from tavily import TavilyClient
        tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        results = tavily.search(
            query=claim,
            search_depth="advanced",
            max_results=5,
            include_answer=True
        )
        sources = []
        for r in results.get("results", []):
            url = r.get("url", "")
            if url:
                sources.append({
                    "title": r.get("title", "Unknown source"),
                    "url": url,
                    "snippet": r.get("content", "")[:400],
                    "source": "tavily"
                })
        return sources
    except Exception as e:
        print(f"Tavily error: {e}")
        return []


def _search_duckduckgo(claim: str) -> list:
    """Search using DuckDuckGo (free, no API key needed)."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; FactChecker/1.0)"
        }
        params = {
            "q": claim,
            "format": "json",
            "no_html": "1",
            "skip_disambig": "1"
        }
        resp = requests.get(
            "https://api.duckduckgo.com/",
            params=params,
            headers=headers,
            timeout=8
        )
        data = resp.json()
        sources = []

        # Abstract (main answer)
        if data.get("AbstractURL") and data.get("AbstractText"):
            sources.append({
                "title": data.get("AbstractSource", "DuckDuckGo Abstract"),
                "url": data["AbstractURL"],
                "snippet": data["AbstractText"][:400],
                "source": "duckduckgo"
            })

        # Related topics
        for topic in data.get("RelatedTopics", [])[:6]:
            if isinstance(topic, dict) and topic.get("FirstURL") and topic.get("Text"):
                sources.append({
                    "title": topic.get("Text", "")[:60],
                    "url": topic["FirstURL"],
                    "snippet": topic.get("Text", "")[:400],
                    "source": "duckduckgo"
                })

        # DuckDuckGo HTML search fallback for more results
        if len(sources) < 3:
            params2 = {"q": claim, "format": "json", "no_redirect": "1"}
            resp2 = requests.get(
                "https://html.duckduckgo.com/html/",
                params={"q": claim},
                headers={**headers, "Accept": "text/html"},
                timeout=8
            )
            # Parse basic results from HTML
            from html.parser import HTMLParser

            class DDGParser(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.results = []
                    self.in_result = False
                    self.current = {}

                def handle_starttag(self, tag, attrs):
                    attrs = dict(attrs)
                    if tag == "a" and "result__a" in attrs.get("class", ""):
                        self.in_result = True
                        href = attrs.get("href", "")
                        if href.startswith("http"):
                            self.current["url"] = href
                    if tag == "a" and "result__snippet" in attrs.get("class", ""):
                        self.in_snippet = True

                def handle_data(self, data):
                    if self.in_result and "url" in self.current and "title" not in self.current:
                        self.current["title"] = data.strip()
                        self.in_result = False
                        if self.current.get("url"):
                            self.results.append(dict(self.current))
                            self.current = {}

            try:
                parser = DDGParser()
                parser.feed(resp2.text)
                for r in parser.results[:4]:
                    if r.get("url") and r.get("title"):
                        sources.append({
                            "title": r["title"],
                            "url": r["url"],
                            "snippet": r.get("snippet", r["title"]),
                            "source": "duckduckgo"
                        })
            except Exception:
                pass

        return sources
    except Exception as e:
        print(f"DuckDuckGo error: {e}")
        return []


def _deduplicate(sources: list) -> list:
    """Remove duplicate URLs, keep first occurrence."""
    seen_urls = set()
    seen_domains = set()
    unique = []
    for s in sources:
        url = s.get("url", "").strip().rstrip("/")
        if not url:
            continue
        # Extract domain
        try:
            domain = url.replace("https://","").replace("http://","").split("/")[0]
        except Exception:
            domain = url
        # Skip exact URL duplicates
        if url in seen_urls:
            continue
        # Skip same-domain duplicates (keep max 2 per domain)
        domain_count = sum(1 for u in seen_urls if domain in u)
        if domain_count >= 2:
            continue
        seen_urls.add(url)
        unique.append(s)
    return unique


def search_claim(claim: str) -> list:
    """Search both Tavily and DuckDuckGo, merge and deduplicate results."""
    tavily_results = _search_tavily(claim)
    ddg_results    = _search_duckduckgo(claim)

    # Interleave: tavily first (higher quality), then DDG fills gaps
    combined = tavily_results + ddg_results
    unique   = _deduplicate(combined)

    # Return up to 8 sources
    return unique[:8]
