# Fintech Risk Agent 🤖💰

An autonomous AI agent for assessing loan default risk using **Explainable AI (XAI)**, **Retrieval-Augmented Generation (RAG)**, and a **Contract-Driven API**.

## 🚀 Features

*   **Logic-Aware Training**: Uses `class_weight='balanced'` Random Forest to handle imbalanced default data.
*   **Business Metric Optimization**: Prioritizes **Recall** (catching bad loans) over raw accuracy.
*   **RAG Compliance**: Retrieves dynamic rules from `rag/policies.txt` (e.g., DTI limits, Credit Score thresholds) to validate decisions.
*   **Explainability**: Generates human-readable reports linking model probability + feature data + policy rules.
*   **Contract-Driven API**: Fully typed FastAPI endpoints with strict schema validation.
*   **Human-in-the-Loop**: Interactive CLI for officers to review and override high-risk flags.

## 📂 Project Structure

```
fintech-risk-agent/
├── agent/
│   ├── agent.py       # Core loop (Train -> Eval -> Explain)
├── api/
│   ├── contracts.py   # 📜 API Pydantic Models (Schema Definition)
│   ├── server.py      # 🌐 FastAPI Application Logic
├── tools/
│   ├── train_tool.py  # Model training logic with sklearn
│   ├── eval_tool.py   # Precision/Recall metrics
│   ├── explain_tool.py# RAG retrieval + LLM-style explanation generation
│   └── data_tool.py   # Data ingestion
├── rag/
│   └── policies.txt   # 📜 Editable bank policies (DTI, Credit Score rules)
├── data/
│   └── loan_data.csv  # Synthetic training data
└── main.py            # 🖥️ CLI Entry Point
```

## 🛠️ Installation

1.  **Environment**:
    ```bash
    python -m venv .venv
    .venv\Scripts\activate  # Windows
    pip install pandas scikit-learn joblib fastapi uvicorn
    ```

2.  **Usage (CLI)**:

    Run the full autonomous loop:
    ```bash
    python main.py
    ```

    Run specific modules:
    ```bash
    python main.py train        # Retrain model
    python main.py eval         # Check metrics
    python main.py interactive  # Start Human-in-the-Loop review
    ```

3.  **Usage (API)**:

    Start the server:
    ```bash
    python main.py api
    ```

    **Endpoint**: `POST /assess-risk`
    
    **Example Payload**:
    ```json
    {
      "income": 85000,
      "credit_score": 720,
      "loan_amount": 15000,
      "employment_years": 5,
      "dti": 0.25,
      "loan_term": 36
    }
    ```

    **Response**:
    ```json
    {
      "decision": "APPROVE",
      "risk_score": 0.12,
      "risk_level": "Low",
      "explanation": "..."
    }
    ```

## ⚙️ System Parameters

### Model Configuration (`tools/train_tool.py`)
*   **Algorithm**: Random Forest Classifier
*   **Estimators**: `200`
*   **Class Weight**: `balanced` (Critical for detecting defaults)

### Risk Thresholds (`agent/agent.py`)
*   **Recall Alert**: `< 0.70` (Triggers "Model needs improvement")
*   **Precision Alert**: `< 0.60` (Triggers "Too many false alarms")

### RAG Policies (`rag/policies.txt`)
*   **DTI Critical**: `> 0.50`
*   **Credit Score Auto-Reject**: `< 550`
*   **Manual Review**: Loan > $40k AND Score < 650

## 📝 License
MIT
