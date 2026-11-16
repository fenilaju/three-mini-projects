# Login and Registration

Simple Flask login and registration application with SQLite persistence. Passwords are hashed with Werkzeug; successful registration logs the user in.

## Run

```bash
python -m venv .venv
# Activate the virtual environment, then:
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000. Accounts are stored in `users.db`, created automatically. Set `SECRET_KEY` to a long random value outside local demos. This starter is not production hardened.
