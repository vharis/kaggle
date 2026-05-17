"""
Diabetes Risk Analyzer — Streamlit Frontend
Calls the FastAPI ML service at localhost:8000/predict,
then uses OpenAI to generate a plain-language health explanation.
"""

import os
import requests
import streamlit as st

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Diabetes Risk Analyzer",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Styles ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .block-container { padding-top: 2rem; }
    .risk-high {
        background:#ff6b6b; color:white; padding:18px 24px;
        border-radius:10px; font-size:20px; font-weight:700; text-align:center;
    }
    .risk-low {
        background:#51cf66; color:white; padding:18px 24px;
        border-radius:10px; font-size:20px; font-weight:700; text-align:center;
    }
    .disclaimer {
        font-style:italic; color:#888; font-size:13px;
        border-top:1px solid #eee; padding-top:10px; margin-top:20px;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("## 🏥 Diabetes Risk Analyzer")
st.markdown(
    "Enter your health metrics and click **Analyze Risk** for an instant ML-powered "
    "assessment plus a personalized explanation."
)
st.markdown("---")

API_URL = os.environ.get("ML_API_URL", "http://localhost:8000/predict")

# ── Input form ────────────────────────────────────────────────────────────────
with st.form("risk_form"):
    col1, col2 = st.columns(2)

    with col1:
        age = st.slider("👤 Age (years)", min_value=18, max_value=100, value=45, step=1)
        glucose = st.slider(
            "🩸 Glucose Level (mg/dL)", min_value=50, max_value=300, value=120, step=1
        )

    with col2:
        bmi = st.slider(
            "⚖️ BMI (kg/m²)", min_value=10.0, max_value=60.0, value=25.0, step=0.1,
            format="%.1f"
        )
        dpf = st.slider(
            "🧬 Diabetes Pedigree Function", min_value=0.0, max_value=3.0,
            value=0.45, step=0.01, format="%.2f",
            help="A function that scores likelihood of diabetes based on family history."
        )

    submitted = st.form_submit_button(
        "🔍 Analyze Risk", use_container_width=True, type="primary"
    )

# ── Prediction flow ───────────────────────────────────────────────────────────
if submitted:
    # 1. Call ML API
    with st.spinner("Contacting ML service…"):
        try:
            resp = requests.post(
                API_URL,
                json={
                    "age": age,
                    "bmi": bmi,
                    "glucose": glucose,
                    "diabetic_pedigree_function": dpf,
                },
                timeout=15,
            )
            resp.raise_for_status()
            result = resp.json()
        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot reach the ML API. Make sure `python ml_service.py` is "
                "running in a separate terminal."
            )
            st.stop()
        except Exception as e:
            st.error(f"API error: {e}")
            st.stop()

    prediction = result["prediction"]
    confidence = result["confidence"]
    model_used = result.get("model_used", "unknown")

    # 2. Display result banner
    st.markdown("### 🎯 Risk Assessment")
    if prediction == 1:
        st.markdown(
            f"<div class='risk-high'>⚠️ HIGH RISK — Confidence: {confidence*100:.1f}%</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div class='risk-low'>✅ LOW RISK — Confidence: {confidence*100:.1f}%</div>",
            unsafe_allow_html=True,
        )

    st.caption(f"Classifier: {model_used}")
    st.markdown("---")

    # 3. LLM explanation
    openai_key = (
        os.environ.get("OPENAI_API_KEY")
        or st.secrets.get("OPENAI_API_KEY", "")
        if hasattr(st, "secrets")
        else ""
    )

    if not openai_key:
        st.info(
            "**Tip:** Set the `OPENAI_API_KEY` environment variable (or add it to "
            "Streamlit secrets) to receive a personalized plain-language explanation."
        )
    else:
        with st.spinner("Generating personalized health explanation…"):
            try:
                from openai import OpenAI

                client = OpenAI(api_key=openai_key)

                risk_text = "HIGH diabetes risk" if prediction == 1 else "LOW diabetes risk"
                prompt = (
                    f"You are a warm and supportive health assistant. "
                    f"A patient has shared these metrics:\n"
                    f"- Age: {age} years\n"
                    f"- BMI: {bmi:.1f} kg/m²\n"
                    f"- Fasting Glucose: {glucose} mg/dL\n"
                    f"- Diabetes Pedigree Function: {dpf:.2f}\n\n"
                    f"A machine-learning model predicted {risk_text} "
                    f"(confidence {confidence*100:.1f}%).\n\n"
                    f"In 2–3 short paragraphs:\n"
                    f"1. Explain in plain language what these numbers mean.\n"
                    f"2. Offer 3–4 friendly, actionable wellness tips tailored to this "
                    f"risk level.\n"
                    f"3. Close with encouragement.\n\n"
                    f"Keep the tone warm, supportive, and free of medical jargon."
                )

                chat = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=600,
                )
                explanation = chat.choices[0].message.content

            except Exception as e:
                explanation = None
                st.warning(f"Could not generate explanation: {e}")

        if explanation:
            st.markdown("### 💬 Personalized Health Explanation")
            st.markdown(explanation)

            st.markdown(
                "<div class='disclaimer'>"
                "⚠️ <strong>Medical Disclaimer:</strong> This is an informational AI tool "
                "and does not constitute professional medical advice, diagnosis, or treatment. "
                "Always consult a qualified healthcare provider for medical concerns."
                "</div>",
                unsafe_allow_html=True,
            )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:gray;font-size:12px;'>"
    "🏥 Diabetes Risk Analyzer | ML Backend: FastAPI | Frontend: Streamlit"
    "</div>",
    unsafe_allow_html=True,
)
