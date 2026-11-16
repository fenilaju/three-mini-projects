import re
import sys
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; SimpleSiteSummarizer/1.0)"}


def normalize_url(value):
    value = value.strip()
    if not value.startswith(("http://", "https://")):
        value = "https://" + value
    parsed = urlparse(value)
    if not parsed.hostname or "." not in parsed.hostname:
        raise ValueError("Enter a valid domain or URL, such as example.com")
    return value


def extract_text(url):
    response = requests.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    for element in soup(["script", "style", "nav", "footer", "header", "noscript", "svg"]):
        element.decompose()
    title = soup.title.get_text(" ", strip=True) if soup.title else urlparse(url).hostname
    text = re.sub(r"\s+", " ", soup.get_text(" ", strip=True))
    if len(text) < 100:
        raise ValueError("This page has too little readable text to summarize (it may require JavaScript or a login).")
    return title, text[:12000]


def summarize(title, text):
    prompt = f"Summarize this webpage in 4 concise bullet points. Do not add facts that are not present.\n\nTitle: {title}\nPage text:\n{text}"
    try:
        response = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt, "stream": False}, timeout=60)
        response.raise_for_status()
        summary = response.json().get("response", "").strip()
        if summary:
            return summary + "\n\n(Summarized with Ollama.)"
    except requests.RequestException:
        pass
    sentences = re.split(r"(?<=[.!?])\s+", text)
    picks = [s.strip() for s in sentences if len(s.strip()) > 45][:4]
    return "\n".join(f"• {sentence}" for sentence in picks) + "\n\n(Extractive summary; start Ollama for an LLM summary.)"


def main():
    if len(sys.argv) != 2:
        print("Usage: python app.py <site-name-or-url>\nExample: python app.py example.com")
        raise SystemExit(2)
    try:
        url = normalize_url(sys.argv[1])
        title, text = extract_text(url)
        print(f"\n{title}\n{'=' * len(title)}\n")
        print(summarize(title, text))
    except (ValueError, requests.RequestException) as exc:
        print(f"Error: {exc}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
