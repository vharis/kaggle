#!/bin/bash
# ─────────────────────────────────────────────────────────
#  Diabetes Risk Analyzer — Local Setup Script
# ─────────────────────────────────────────────────────────

set -e

echo "==========================================="
echo " Diabetes Risk Analyzer — Setup"
echo "==========================================="

# 1. Create virtual environment
if [ ! -d ".venv" ]; then
    echo "▶ Creating virtual environment (.venv)…"
    python3 -m venv .venv
else
    echo "✓ .venv already exists"
fi

# 2. Activate
echo "▶ Activating virtual environment…"
source .venv/bin/activate

# 3. Upgrade pip silently
pip install --upgrade pip -q

# 4. Install all dependencies
echo "▶ Installing dependencies…"
pip install \
    streamlit \
    fastapi \
    "uvicorn[standard]" \
    scikit-learn \
    pandas \
    numpy \
    requests \
    openai \
    joblib \
    -q

echo "✓ Dependencies installed"

# 5. Train the 4-feature API model if not already present
if [ ! -f "model.pkl" ]; then
    echo "▶ Training ML model (this takes ~10 seconds)…"
    python3 -c "
from ml_service import train_and_save
train_and_save()
"
    echo "✓ model.pkl saved"
else
    echo "✓ model.pkl already exists"
fi

echo ""
echo "==========================================="
echo " Setup Complete!"
echo "==========================================="
echo ""
echo "┌─────────────────────────────────────────┐"
echo "│  HOW TO RUN (use two separate terminals) │"
echo "└─────────────────────────────────────────┘"
echo ""
echo "▶ TERMINAL 1 — ML API backend (FastAPI):"
echo "    source .venv/bin/activate"
echo "    python ml_service.py"
echo "    → Runs on http://localhost:8000"
echo "    → API docs: http://localhost:8000/docs"
echo ""
echo "▶ TERMINAL 2 — Streamlit frontend:"
echo "    source .venv/bin/activate"
echo "    streamlit run app.py"
echo "    → Opens http://localhost:8501"
echo ""
echo "▶ (Optional) Set your OpenAI API key for LLM explanations:"
echo "    export OPENAI_API_KEY=sk-..."
echo ""
