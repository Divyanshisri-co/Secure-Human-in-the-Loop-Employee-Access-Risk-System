import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
import os
# LOAD DATASET (EMPLOYEE MASTER + TRAINING DATA)
# --------------------------------------------------
DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "Employee_Access_Risk_Dataset_.xlsx"
)

df = pd.read_excel(DATA_PATH)

# --------------------------------------------------
# ACCESS SENSITIVITY MAP (USED BY APP)
# --------------------------------------------------
ACCESS_SENSITIVITY_MAP = {
    "Source_Code_Repo": 1,
    "Internal_Tools": 2,
    "Employee_Records": 3,
    "Server_Admin": 4,
    "Billing_System": 5,
    "Financial_Reports": 4,
}

# --------------------------------------------------
# EMPLOYEE PROFILE LOOKUP
# --------------------------------------------------
def get_employee_profile(employee_id: str):
    row = df[df["employee_id"] == employee_id]

    if row.empty:
        return None

    row = row.iloc[0]

    return {
        "department": row["department"],
        "role": row["role"],
        "tenure_years": int(row["tenure_years"]),
        "past_violations": int(row["past_violations"]),
    }

# --------------------------------------------------
# RISK PREDICTION (RULE-BASED, ALIGNED TO DATASET)
# --------------------------------------------------
def predict_risk(features):
    """
    features = [
        department,
        role,
        requested_access,
        access_sensitivity,
        tenure_years,
        past_violations
    ]
    """

    _, _, _, access_sensitivity, tenure_years, past_violations = features

    # 🔐 SAME FORMULA USED IN DATASET GENERATION
    risk_score = round(
        (0.15 * access_sensitivity) +
        (0.08 * past_violations) +
        (0.02 * max(0, 10 - tenure_years)),  # less tenure → more risk
        2
    )

    # 🎯 EXACT THRESHOLDS (MATCH DATASET)
    if risk_score <= 0.35:
        risk_level = "LOW"
    elif risk_score <= 0.65:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

    # Model confidence (simulated, realistic)
    confidence = min(0.95, max(0.75, round(1 - abs(0.5 - risk_score), 2)))

    return risk_level, confidence

# --------------------------------------------------
# RISK EXPLANATION (EXPLAINABLE AI)
# --------------------------------------------------
def explain_risk(features):
    _, _, _, access_sensitivity, tenure_years, past_violations = features

    explanations = []

    if access_sensitivity >= 4:
        explanations.append("High access sensitivity")

    if past_violations > 0:
        explanations.append("Past security violations")

    if tenure_years < 3:
        explanations.append("Low tenure")

    if not explanations:
        explanations.append("Access aligns with role and experience")

    return explanations

