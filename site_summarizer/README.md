# Website Summarizer

Enter a site name or URL to fetch the page, remove navigation and scripts, and summarize its readable text. Uses a local Ollama LLM when available and a simple extractive fallback otherwise.

## Run

```bash
pip install -r requirements.txt
ollama pull llama3.2   # optional; requires Ollama installed and running
python app.py example.com
```

You can also provide a full URL: `python app.py https://example.com/about`. Some sites block automated requests, require JavaScript, or require a login. Only summarize pages you are allowed to access.
