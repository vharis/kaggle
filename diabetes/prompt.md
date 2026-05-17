Act as an expert Data Scientist and Full-Stack Python Developer. I need you to create a complete, end-to-end Machine Learning and Streamlit application for a Diabetes Risk Predictor.

The application must follow a simple, decoupled architecture: a backend ML API service, a Streamlit frontend GUI, and an OpenAI LLM integration for natural language explanation.

### IMPORTANT CONTEXT:

In the current directory, there are a few components already built in an earlier attempt. Please scan and make use of these existing artifacts as much as possible to maintain continuity and avoid over-engineering or rewriting functional code from scratch.

Please provide the solution across the following distinct parts, keeping the final additions clean, modular, and easy to integrate:

---

### PART 1: ML Model Training & Public API Service (`ml_service.py`)

1. **Model Training Logic:**
   - Write code that reads a local dataset named `diabetes.csv`.
   - Preprocess the data, selecting the key features: `Glucose`, `BMI`, `DiabetesPedigreeFunction`, and `Age`.
   - Train a highly accurate classifier (such as a Random Forest or Logistic Regression model using scikit-learn). Save the trained model and any scaler used to disk (e.g., `model.pkl`).
2. **Prediction Function:**

- Create a clean Python function named `predict_diabetes(glucose, bmi, dpf, age)`.
- Inside this function, load the `model.pkl` file, pass the input arguments into the model, and return the binary prediction (0 or 1) along with the confidence probability.
- Include a fallback check: if `model.pkl` is missing, use a simple logical rule-base so the function can still execute and return a fallback result during initial testing.

### PART 2 & 3: Streamlit Frontend & LLM Integration (`app.py`)

1. **User Interface:**
   - Create a clean Streamlit form to accept numeric/slider inputs for: Age, BMI, Glucose, and Diabetes Pedigree Function.
2. **High-Level Flow Logic:**
   - When the user clicks "Analyze Risk", the app must send a `requests.post` call to the Part-1 ML API service.
   - Parse the prediction results.
   - Pass the original metrics and the ML prediction data to the OpenAI API (using the standard `openai` library with `os.environ` or `st.secrets["OPENAI_API_KEY"]`).
3. **LLM Prompting & Display:**
   - Prompt the OpenAI model to act as a supportive health assistant. It should interpret the numbers in plain language and offer friendly wellness advice based on the risk level.
   - **Mandatory:** End the LLM output with a prominent, italicized medical disclaimer stating this is an informational AI tool, not professional medical advice.
   - Render the narrative output dynamically using `st.markdown`.

---

### PART 4: Local Automation Setup (`setup.sh`)

Provide a complete bash script named `setup.sh` that automates local testing in a virtual environment. The script must:

1. Create a local Python virtual environment (`.venv`).
2. Activate the virtual environment.
3. Install all required dependencies (`streamlit`, `fastapi`, `uvicorn`, `scikit-learn`, `pandas`, `requests`, `openai`).
4. Print clear instructions to the terminal on how to run the backend API service and the Streamlit app simultaneously in separate terminal windows.

---

### PART 5: Streamlit Cloud Deployment Instructions

Provide a step-by-step Markdown guide detailing exactly how to deploy this Streamlit frontend to the Streamlit Community Cloud, making it publicly accessible, including how to safely store the OpenAI API Key in the cloud dashboard settings.
