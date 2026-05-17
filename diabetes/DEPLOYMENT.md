# Deploying to Streamlit Community Cloud

This guide covers deploying the **Streamlit frontend** (`app.py`) to the public
[Streamlit Community Cloud](https://streamlit.io/cloud) and securely storing your
OpenAI API key.

> **Note on the architecture:** Streamlit Cloud runs only the frontend (`app.py`).
> The FastAPI ML backend (`ml_service.py`) must be hosted separately (e.g. Railway,
> Render, Fly.io, or any always-on server). Point `ML_API_URL` in Streamlit secrets
> to wherever you deploy the backend.

---

## Prerequisites

- A **GitHub** account
- A **Streamlit Community Cloud** account (free at https://streamlit.io/cloud)
- Your FastAPI backend deployed and reachable via a public URL

---

## Step 1 — Push the project to GitHub

```bash
# From the project root
git init
git add app.py requirements.txt .streamlit/
git commit -m "Initial commit: Streamlit diabetes app"

# Create a new repo on github.com, then:
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

> Keep `model.pkl`, `diabetes_env/`, and `.venv/` out of the repo — they are
> already listed in `.gitignore`.

---

## Step 2 — Connect to Streamlit Community Cloud

1. Go to **https://share.streamlit.io** and sign in with GitHub.
2. Click **"New app"**.
3. Under **Repository**, select the repo you just pushed.
4. Set **Branch** to `main`.
5. Set **Main file path** to `app.py`.
6. Click **"Advanced settings"** (expand the section).

---

## Step 3 — Store secrets safely

In the **Advanced settings → Secrets** text box, add:

```toml
OPENAI_API_KEY = "sk-..."
ML_API_URL = "https://your-backend.example.com/predict"
```

- These are stored encrypted by Streamlit and exposed to your app via `st.secrets`.
- **Never commit API keys to Git.**

---

## Step 4 — Deploy

Click **"Deploy!"**

Streamlit will:
1. Clone your repo.
2. Install packages from `requirements.txt`.
3. Start `app.py`.

Your app will be live at:
```
https://<your-username>-<repo-name>-<random>.streamlit.app
```

---

## Step 5 — Deploy the FastAPI backend (recommended: Render)

1. Push `ml_service.py`, `requirements.txt`, and `diabetes.csv` to a GitHub repo
   (can be the same repo or a separate one).
2. Go to **https://render.com** → **New Web Service**.
3. Connect your GitHub repo.
4. Set:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `python ml_service.py`
5. After deploy, copy the public URL (e.g. `https://diabetes-api.onrender.com`).
6. Update your Streamlit secret `ML_API_URL` to point to this URL + `/predict`.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| "Cannot reach the ML API" | Make sure `ML_API_URL` in secrets points to the live backend |
| "Import openai could not be resolved" | Verify `openai` is in `requirements.txt` |
| App crashes on startup | Check the Streamlit Cloud logs (Manage app → Logs) |
| OpenAI quota error | Check your OpenAI billing at platform.openai.com |

---

## Security checklist

- [x] OpenAI key stored in Streamlit secrets, not in code
- [x] Backend URL stored in secrets, not hardcoded
- [x] `model.pkl` and data files excluded from Git via `.gitignore`
- [ ] (Optional) Add CORS restrictions and an API key to the FastAPI backend for production
