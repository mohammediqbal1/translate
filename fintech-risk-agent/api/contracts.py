from pydantic import BaseModel, Field

class LoanApplication(BaseModel):
    income: float = Field(..., description="Annual income in USD", gt=0)
    credit_score: int = Field(..., description="FICO Credit Score (300-850)", ge=300, le=850)
    loan_amount: float = Field(..., description="Requested loan amount in USD", gt=0)
    employment_years: int = Field(..., description="Years at current employment", ge=0)
    dti: float = Field(..., description="Debt-to-Income Ratio (e.g., 0.45)", ge=0.0, le=1.0)
    loan_term: int = Field(..., description="Loan term in months", ge=12, le=360)

class RiskAssessment(BaseModel):
    decision: str = Field(..., description="Final decision: 'APPROVE' or 'REJECT'")
    risk_score: float = Field(..., description="Probability of default (0.0 - 1.0)")
    risk_level: str = Field(..., description="Risk categorization (Low, Medium, High)")
    explanation: str = Field(..., description="AI-generated reason including policy alerts")
