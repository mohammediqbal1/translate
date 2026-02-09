import pandas as pd
import joblib
import sys
from tools.train_tool import train_model
from tools.eval_tool import evaluate_model
from tools.explain_tool import generate_explanation

class RiskAgent:
    def __init__(self, data_path="data/loan_data.csv", model_path="models/risk_model.pkl"):
        self.data_path = data_path
        self.model_path = model_path
        self.model = None

    def train(self):
        print("\n[AGENT] 🏋️ Training model...")
        X_test, y_test = train_model(self.data_path)
        print("✅ Training complete. Model saved.")
        return X_test, y_test

    def evaluate(self):
        print("\n[AGENT] 📊 Evaluating model...")
        X_test, y_test = train_model(self.data_path) # Re-split to get test set
        self.model = joblib.load(self.model_path)
        preds = self.model.predict(X_test)
        metrics = evaluate_model(y_test, preds)
        print(f"   Precision: {metrics['precision']:.2f}")
        print(f"   Recall:    {metrics['recall']:.2f}")
        print(f"   Accuracy:  {metrics['accuracy']:.2f}")
        
        # Threshold Checks
        if metrics['recall'] < 0.7:
            print("⚠️  WARNING: Recall is below 0.7! High risk of missing defaults.")
        elif metrics['precision'] < 0.6:
            print("⚠️  WARNING: Precision is low. Expect false alarms.")
        else:
            print("✅ Model performance is within acceptable risk parameters.")

    def run_interactive(self):
        print("\n[AGENT] 🕵️ Starting Interactive Risk Review...")
        X_test, y_test = train_model(self.data_path)
        self.model = joblib.load(self.model_path)
        preds = self.model.predict(X_test)
        probs = self.model.predict_proba(X_test)
        
        found_risky = False
        print(f"Scanning {len(X_test)} applications for high risk...")
        
        for i in range(len(X_test)):
            prediction = preds[i]
            if prediction == 1: # High Risk
                found_risky = True
                features = X_test.iloc[i].to_dict()
                prob_default = probs[i][1]
                
                explanation = generate_explanation(features, prediction, prob_default)
                
                print(f"\n{'='*60}")
                print(f"🚨 ALERT: HIGH RISK APPLICATION DETECTED (ID: {i})")
                print(f"{'='*60}")
                print(explanation)
                print(f"{'='*60}")
                
                print("\n👤 HUMAN DECISION REQUIRED")
                try:
                    action = input(">>> [A]pprove, [R]eject, or [S]kip? ").strip().lower()
                except EOFError:
                    action = 's'
                
                if action == 'a':
                    print("✅ APPROVED [Override Logged]")
                elif action == 'r':
                    print("❌ REJECTED [Confirmed]")
                else:
                    print("⏩ Skipped.")
        
        if not found_risky:
            print("✅ No high-risk applications found in this batch.")

    def run_all(self):
        self.train()
        self.evaluate()
        self.run_interactive()
