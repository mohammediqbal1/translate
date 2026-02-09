import random

def retrieve_policy(features):
    """
    RAG retrieval simulation based on features.
    """
    credit_score = features.get('credit_score', 0)
    loan_amount = features.get('loan_amount', 0)
    dti = features.get('dti', 0)
    term = features.get('loan_term', 0)
    
    policies = []
    with open("rag/policies.txt", "r") as f:
        all_policies = f.readlines()
    
    relevant = []
    
    # Simple semantic search simulation (keyword + logic matching)
    for p in all_policies:
        p_lower = p.lower()
        
        # Credit Score Rules
        if "credit_score" in p_lower:
            if credit_score < 650 and "< 650" in p:
                relevant.append(p.strip())
            if credit_score < 550 and "< 550" in p:
                relevant.append(p.strip())
            if credit_score > 720 and "> 720" in p:
                relevant.append(p.strip())

        # Loan Amount Rules
        if "amount" in p_lower and loan_amount > 40000 and "40000" in p:
             relevant.append(p.strip())

        # DTI Rules
        if "dti" in p_lower:
            if dti > 0.50 and "> 0.50" in p:
                relevant.append(p.strip())
            if dti > 0.43 and "> 0.43" in p:
                relevant.append(p.strip())

        # Employment Rules
        if "employment" in p_lower:
            emp = features.get('employment_years', 0)
            if emp < 2 and "< 2" in p:
                relevant.append(p.strip())

    if not relevant:
        return "No specific policy warnings found."
    return "\n    - " + "\n    - ".join(relevant)

def generate_explanation(features, prediction, probability):
    """
    Simulates an LLM explanation by combining features, prediction, and RAG policies.
    """
    income = features.get('income', 0)
    credit = features.get('credit_score', 0)
    loan = features.get('loan_amount', 0)
    dti = features.get('dti', 0)
    
    risk_level = "High" if prediction == 1 else "Low"
    policy_context = retrieve_policy(features)
    
    explanation = f"""
    Risk Assessment: {risk_level} Risk
    Confidence: {probability:.2%}
    
    Key Risk Factors:
    - Credit Score: {credit}
    - DTI Ratio: {dti:.2f} (Debt-to-Income)
    - Loan Amount: ${loan:,}
    
    Compliance & Policy Check (RAG Retrieval):
    {policy_context}
    
    AI Reasoning:
    The applicant is flagged as {risk_level} risk. 
    {'High DTI suggests debt burden.' if dti > 0.4 else 'DTI is within healthy limits.'}
    {'Credit score is a major concern.' if credit < 600 else 'Credit history is solid.'}
    """
    
    return explanation.strip()
