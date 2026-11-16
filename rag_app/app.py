from pathlib import Path
import requests
from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE = Path(__file__).resolve().parent
DOCS = BASE / "documents"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"
app = Flask(__name__)


def load_chunks():
    chunks = []
    for path in DOCS.glob("*.txt"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for start in range(0, len(text), 700):
            part = text[start:start + 700].strip()
            if part:
                chunks.append((path.name, part))
    return chunks


def retrieve(question, chunks, count=3):
    if not chunks:
        return []
    corpus = [chunk for _, chunk in chunks] + [question]
    matrix = TfidfVectorizer(stop_words="english").fit_transform(corpus)
    scores = cosine_similarity(matrix[-1], matrix[:-1]).ravel()
    indexes = scores.argsort()[::-1][:count]
    return [(chunks[i][0], chunks[i][1]) for i in indexes if scores[i] > 0]


def answer(question, matches):
    if not matches:
        return "I couldn't find a relevant passage. Add .txt files to the documents folder and try again."
    context = "\n\n".join(f"[{name}] {text}" for name, text in matches)
    prompt = f"Answer the question using only the context. If the context does not contain the answer, say so.\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer:"
    try:
        response = requests.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt, "stream": False}, timeout=45)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except requests.RequestException:
        return "Ollama isn't available, so here are the closest retrieved passages:\n\n" + "\n\n".join(f"From {name}: {text}" for name, text in matches)


@app.route("/", methods=["GET", "POST"])
def index():
    question = request.form.get("question", "").strip()
    matches, result = [], ""
    if question:
        matches = retrieve(question, load_chunks())
        result = answer(question, matches)
    return render_template("index.html", question=question, matches=matches, result=result)


if __name__ == "__main__":
    DOCS.mkdir(exist_ok=True)
    app.run(debug=True, port=5001)
