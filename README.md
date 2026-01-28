# Secure-Human-in-the-Loop-Employee-Access-Risk-System
📌 Project Overview

This project implements a Secure Employee Access Management System using Machine Learning and Human-in-the-Loop (HITL) principles.
The system intelligently decides whether an employee’s access request should be:
---Automatically approved (low risk).
---Escalated for human review (medium/high risk).

The goal is to balance security and efficiency by combining automation with human judgment.

🎯 Key Objectives

--Prevent unauthorized or risky access.
--Reduce manual workload for security teams.
--Provide explainable and auditable access decisions.
--Demonstrate real-world HITL security architecture.

🧠 Core Concepts Used

Human-in-the-Loop (HITL)	--> Human review for risky decisions
Role-Based Access Control (RBAC)	--> Employee, Reviewer, Admin roles
Risk Scoring	--> ML-based access risk evaluation
Explainable AI (XAI)	--> Shows top risk factors
Separation of Duties	--> Reviewer ≠ Admin
Least Privilege	--> Only necessary access granted

🏗️ System Workflow

1️⃣ Employee Flow

1. Employee logs in
2. Requests access to a system
3. System automatically:
----Fetches employee profile
----Calculates risk score
4. If Low Risk → Auto Approved
5. If Medium / High Risk → Sent to Reviewer

2️⃣ Reviewer Flow

1. Reviewer logs in
2. Sees only pending risky requests
3. Reviews:
----Risk level
----Confidence
----Top risk factors
4. Approves or rejects request

3️⃣ Admin Flow

1. Admin logs in
2. Views:
----All access requests
----Reviewer decisions
----System metrics
3. Can override decisions if needed

--🔁 Decision Logic
Low Risk      → Auto Approve
Medium Risk   → Human Review
High Risk     → Human Review

📊 Risk Factors Considered

1. Employee department
2. Job role
3. Requested access type
4. Access sensitivity
5. Employee tenure
6. Past policy violations
⚠️ Employees cannot modify these values.

🧪 Tools & Technologies Used

🖥️ Backend & UI
1. Python
2. Streamlit (Web UI)

🗄️ Database

1. SQLite
2. Tables:
--users
--access_requests

🤖 Machine Learning

1. Rule-based / ML-inspired risk model
2. Explainable outputs (top risk factors)

🛠️ Skills Demonstrated

1. Secure system design
2. Access control models
3. HITL architecture
4. Python application development
5. Database schema design
6. Risk modeling
7. Explainable AI
8. Role-based authentication
9. Real-world security workflows

📁 Project Structure

secure-hitl-employee-access/
│
├── src/
│   ├── app.py              # Main Streamlit app
│   ├── auth.py             # Authentication & RBAC
│   ├── db.py               # Database operations
│   ├── risk_model.py       # Risk scoring & explanation
│   ├── init_db.py          # DB & table creation
│   ├── create_user.py      # Insert users
│
├── db.sqlite               # SQLite database
├── README.md               # Project documentation

✅ Before Running – Checklist

Make sure the following are done:

✔️ 1. Python Installed & Install Requirements
python --version
Open terminal :
pip install -r requirements.txt

✔️ 2. Required Libraries Installed
pip install streamlit pandas

✔️ 3. Database Initialized
python src/init_db.py
python src/create_user.py


✔️ This should create:

--db.sqlite
--users table
--access_requests table

▶️ How to Run the Project
streamlit run src/app.py

🔑 Default Login Credentials
👤 Employees
Username	-- Password
emp01	-- pass101
emp02	-- pass202
emp03	-- pass303
...	-- ...

🧑‍⚖️ Reviewer
Username: reviewer
Password: review123

👑 Admin
Username: admin
Password: admin123

📈 System Metrics (Admin View)

1. Total requests
2. Auto-approved requests
3. Human reviewed requests
4. Reviewer overrides

🔒 Security Highlights

1. Employees cannot see or edit risk scores
2. RBAC strictly enforced
3. Reviewer and Admin roles separated
4. Explainable risk decisions
5. Manual override only by Admin

🚀 Future Enhancements

1. Integration with HR systems
2. Email / Slack notifications
3. Advanced ML models
4. Access expiry and revocation
5. Visualization dashboards

🧾 Summary

This project demonstrates a practical, enterprise-ready approach to secure access management using automation, machine learning, and human oversight.Not everything should be automated — and not everything should be manual. This system finds the balance.
