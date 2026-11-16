# Document Q&A (RAG)

A small retrieval-augmented generation demo. It splits local text files into chunks, ranks them with TF-IDF, and sends the most relevant context to Ollama. If Ollama is offline, it displays the retrieved passages instead.

## Run

```bash
pip install -r requirements.txt
# Add one or more .txt files to documents/
ollama pull llama3.2   # optional; requires Ollama installed and running
python app.py
```

Open http://127.0.0.1:5001. Change `MODEL` and `OLLAMA_URL` in `app.py` to use another local Ollama model. This uses a local language model and does not require an API key.
