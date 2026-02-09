import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from api.contracts import LoanApplication, RiskAssessment
from tools.explain_tool import generate_explanation

app = FastAPI(
    title="Fintech Risk Assessment API 🏦",
    description="Contract-driven API for autonomous credit risk analysis.",
    version="1.0.0"
)

# Load Model (Lazy Loading Pattern)
MODEL_PATH = "models/risk_model.pkl"
model = None

def load_model():
    global model
    try:
        model = joblib.load(MODEL_PATH)
        print("✅ Risk Model Loaded Successfully.")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        model = None

@app.on_event("startup")
async def startup_event():
    load_model()

@app.post("/assess-risk", response_model=RiskAssessment)
async def assess_risk(application: LoanApplication):
    if not model:
        raise HTTPException(status_code=503, detail="Risk Model not loaded. Please train first.")
    
    # Transform Pydantic model to DataFrame for prediction
    features = application.dict()
    df = pd.DataFrame([features])
    
    # Ensure column order matches training data (critical for sklearn)
    required_cols = ["income", "credit_score", "loan_amount", "employment_years", "dti", "loan_term"]
    
    # Validate Columns (though Pydantic does schema, DataFrame order needs to be exact)
    try:
        df = df[required_cols]
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing feature columns: {e}")

    # Predict
    try:
        prediction = model.predict(df)[0]
        probability = model.predict_proba(df)[0][1] # Probability of Default (1)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")

    # Business Logic Wrapper
    risk_level = "High" if prediction == 1 else "Low"
    decision = "REJECT" if risk_level == "High" else "APPROVE"
    
    # Generate Explanation (XAI + RAG)
    explanation_text = generate_explanation(features, prediction, probability)
    
    return RiskAssessment(
        decision=decision,
        risk_score=round(probability, 4),
        risk_level=risk_level,
        explanation=explanation_text
    )

@app.get("/health")
async def health_check():
    return {"status": "active", "model_loaded": model is not None}
