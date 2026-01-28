import streamlit as st
import pandas as pd
from datetime import datetime
from init_db import init_db
from auth import authenticate
from db import (
    get_connection,
    save_request,
    log_action,
)
from risk_model import (
    predict_risk,
    explain_risk,
    get_employee_profile,
    ACCESS_SENSITIVITY_MAP,
)

# --------------------------------------------------
# INIT
# --------------------------------------------------
st.set_page_config(page_title="Secure HITL Access System", layout="wide")
init_db()

# --------------------------------------------------
# LOGOUT
# --------------------------------------------------
def logout():
    st.session_state.clear()
    st.rerun()

# --------------------------------------------------
# LOGIN
# --------------------------------------------------
if "user" not in st.session_state:
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        result = authenticate(username, password)

        if result:
            role, employee_id = result
            st.session_state.user = username
            st.session_state.role = role
            st.session_state.employee_id = employee_id
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.write(f"👤 User: {st.session_state.user}")
st.sidebar.write(f"🔐 Role: {st.session_state.role}")

if st.sidebar.button("🚪 Logout"):
    logout()

# ==================================================
# EMPLOYEE UI
# ==================================================
if st.session_state.role == "employee":
    st.title("👤 Employee Access Request")

    employee_id = st.session_state.employee_id
    st.info(f"Employee ID: {employee_id}")

    requested_access = st.selectbox(
        "Requested Access",
        list(ACCESS_SENSITIVITY_MAP.keys())
    )

    reason = st.text_area("Reason for Access (optional)")

    if st.button("Submit Request"):
        profile = get_employee_profile(employee_id)

        if not profile:
            st.error("Employee profile not found")
            st.stop()

        department = profile["department"]
        role = profile["role"]
        tenure_years = profile["tenure_years"]
        past_violations = profile["past_violations"]

        access_sensitivity = ACCESS_SENSITIVITY_MAP[requested_access]

        risk_level, confidence = predict_risk([
            department,
            role,
            requested_access,
            access_sensitivity,
            tenure_years,
            past_violations
        ])

        explanations = explain_risk([
            department,
            role,
            requested_access,
            access_sensitivity,
            tenure_years,
            past_violations
        ])

        #  AUTO vs HITL
        if risk_level == "LOW":
            status = "APPROVED"
            reviewed_by = "SYSTEM"
            reviewed_at = datetime.now()
            log_action(None, "AUTO_APPROVED_LOW_RISK", "SYSTEM")
            st.success("✅ Access automatically approved (Low Risk)")
        else:
            status = "PENDING"
            reviewed_by = None
            reviewed_at = None
            st.warning("⏳ Request sent for human review")

        save_request((
            employee_id,
            department,
            role,
            requested_access,
            access_sensitivity,
            tenure_years,
            past_violations,
            risk_level,
            confidence,
            ", ".join(explanations),
            status,
            reviewed_by,
            reviewed_at
        ))

    # --------------------------------------------------
    #  EMPLOYEE STATUS VIEW
    # --------------------------------------------------
    st.divider()
    st.subheader("📋 My Access Requests")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT
        id,
        requested_access,
        risk_level,
        status,
        reviewed_by,
        reviewed_at,
        top_risk_factors
    FROM access_requests
    WHERE employee_id = ?
""", (employee_id,))

    rows = cur.fetchall()

    if rows:
        formatted_rows = []
        for r in rows:
            reviewed_at = (
                datetime.strptime(r[5], "%Y-%m-%d %H:%M:%S.%f")
                .strftime("%d/%m/%y %H:%M:%S")
                if r[5] else ""
            )

            formatted_rows.append((
                r[0],
                r[1],
                r[2],
                r[3],
                r[4],
                reviewed_at,
                r[6]
            ))

        columns = [
            "Request ID",
            "Requested Access",
            "Risk Level",
            "Status",
            "Reviewed By",
            "Reviewed At",
            "Risk Explanation"
        ]

        df = pd.DataFrame(formatted_rows, columns=columns)
        st.dataframe(df, use_container_width=True)

    else:
        st.info("No requests submitted yet.")
# ==================================================
#  REVIEWER UI
# ==================================================
elif st.session_state.role == "reviewer":
    st.title("🧑‍⚖️ Reviewer Dashboard")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM access_requests WHERE status='PENDING'")
    rows = cur.fetchall()

    if not rows:
        st.info("No pending requests")

    for r in rows:
        st.subheader(f"Request #{r[0]} | Employee {r[1]}")

        st.write(f"**Department:** {r[2]}")
        st.write(f"**Role:** {r[3]}")
        st.write(f"**Requested Access:** {r[4]}")
        st.write(f"**Tenure:** {r[6]} years")
        st.write(f"**Past Violations:** {r[7]}")

        st.write(f"### 🔐 Risk Level: {r[8]}")
        st.write(f"### 📊 Model Confidence: {round(r[9], 2)}")
        st.warning(f"🔍 Risk Factors: {r[10]}")

        col1, col2 = st.columns(2)

        if col1.button("✅ Approve", key=f"approve_{r[0]}"):
            cur.execute("""
                UPDATE access_requests
                SET status='APPROVED',
                    reviewed_by=?,
                    reviewed_at=?
                WHERE id=?
            """, (st.session_state.user, datetime.now(), r[0]))

            conn.commit()  
            log_action(cur,r[0], "APPROVED", st.session_state.user)
            st.rerun()


        if col2.button("❌ Reject", key=f"reject_{r[0]}"):
            cur.execute("""
                UPDATE access_requests
                SET status='REJECTED',
                    reviewed_by=?,
                    reviewed_at=?
                WHERE id=?
            """, (st.session_state.user, datetime.now(), r[0]))

            conn.commit()  
            log_action(cur,r[0], "REJECTED", st.session_state.user)
            st.rerun()


# ==================================================
# ADMIN UI
# ==================================================
else:
    st.title("👑 Admin Dashboard")

    conn = get_connection()
    cur = conn.cursor()

    # --------------------------------------------------
    # FETCH DATA
    # --------------------------------------------------
    cur.execute("""
        SELECT
            id,
            employee_id,
            requested_access,
            risk_level,
            status,
            reviewed_by,
            reviewed_at
        FROM access_requests
    """)
    rows = cur.fetchall()

    import pandas as pd

    df = pd.DataFrame(
        rows,
        columns=[
            "Request ID",
            "Employee ID",
            "Requested Access",
            "Risk Level",
            "Status",
            "Reviewed By",
            "Reviewed At",
        ]
    )

    if not df.empty:
        df["Reviewed At"] = pd.to_datetime(
            df["Reviewed At"], errors="coerce"
        ).dt.strftime("%d/%m/%y %H:%M:%S")

    # --------------------------------------------------
    # TABLE VIEW
    # --------------------------------------------------
    st.subheader("📋 All Access Requests")
    st.dataframe(df, use_container_width=True)

    # --------------------------------------------------
    # OVERRIDE (TABLE-CONTROLLED)
    # --------------------------------------------------
    st.subheader("🔁 Override Decision")

    eligible_ids = df[
        df["Status"].isin(["APPROVED", "REJECTED"])
    ]["Request ID"].tolist()

    if not eligible_ids:
        st.info("No requests eligible for override")
    else:
        selected_id = st.selectbox(
            "Select Request ID to Override",
            eligible_ids
        )

        if st.button("🔄 Override Selected Request"):
            cur.execute("""
                SELECT status
                FROM access_requests
                WHERE id=?
            """, (selected_id,))
            current_status = cur.fetchone()[0]

            new_status = (
                "REJECTED" if current_status == "APPROVED" else "APPROVED"
            )

            cur.execute("""
                UPDATE access_requests
                SET status=?,
                    reviewed_by=?,
                    reviewed_at=?
                WHERE id=?
            """, (new_status, "admin", datetime.now(), selected_id))

            log_action(
                cur,
                selected_id,
                "OVERRIDDEN_BY_ADMIN",
                "admin"
            )

            conn.commit()
            st.success(
                f"Request {selected_id} overridden → {new_status}"
            )
            st.rerun()

    conn.close()
