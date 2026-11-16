# Three simple Python projects

Three small projects in separate folders. Each project has its own README and dependencies.

## 1. Login and registration (`auth_app`)
Flask + SQLite registration and login with hashed passwords. Run: `cd auth_app`, `pip install -r requirements.txt`, `python app.py`, then open http://127.0.0.1:5000.

## 2. Local document RAG (`rag_app`)
A lightweight retrieval-augmented question answering demo. It indexes local `.txt` files with TF-IDF and sends retrieved context to Ollama (if running); without Ollama it returns the relevant passages. Run: install requirements, put text files in `documents/`, then `python app.py`.

## 3. Website summarizer (`site_summarizer`)
Fetches a public webpage, extracts readable text, and summarizes it with an optional Ollama model or an extractive fallback. Run: install requirements, then `python app.py https://example.com`.

See each folder's README for details. Never deploy the demo login app without adding HTTPS, CSRF protection, rate limiting, and production configuration.