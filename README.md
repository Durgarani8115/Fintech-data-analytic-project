# Personal Finance Tracker with AI Expense Prediction 🚀

An intelligent Personal Finance Tracker that monitors expenses, sets category budgets, and forecasts future spending using Machine Learning. Built with **Django REST Framework**, **React.js (Vite)**, and **scikit-learn / NumPy**.

---

## 🌟 Key Features
- **Real-time Expense Tracking**: Log, search, filter, and categorize daily expenses.
- **AI-Powered Predictive Engine**: Machine Learning regression model that forecasts upcoming 30-day spending per category with confidence ratings and anomaly alerts.
- **Interactive "What-If" Spending Simulator**: Simulate lifestyle or discretionary adjustments and see real-time impact on financial goals.
- **Category Budget Manager**: Set spending limits per category with visual color-coded warnings (under budget, warning, limit exceeded).
- **Savings Milestones**: Target goal tracking with one-click deposits.
- **Visual Analytics**: Dynamic monthly spending velocity charts and interactive category breakdown donut bars.
- **Multi-Currency & Themes**: Instant switching between `$ USD`, `₹ INR`, `€ EUR`, `£ GBP` and Dark/Light modes.

---

## ⚡ Quick Start (Currently Running!)

### 1️⃣ One-Click Run (Windows)
Double-click [`run_project.bat`](file:///d:/Project/Fintech%20college_Project/Personal-Finance-Tracker-with-AI-Expense-Prediction/run_project.bat) to launch both services simultaneously.

---

### 2️⃣ Manual Run Commands

#### Backend (Django REST API)
```bash
cd backend
venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```
- API Base: `http://127.0.0.1:8000/api/`
- Prediction Endpoint: `http://127.0.0.1:8000/api/predict/`
- Analytics Endpoint: `http://127.0.0.1:8000/api/analytics/`

#### Frontend (React + Vite)
```bash
cd frontend
npm run dev
```
- Web Application: `http://127.0.0.1:5173/`

---

## 🏗 Project Architecture
```
Personal-Finance-Tracker-with-AI-Expense-Prediction/
├── backend/
│   ├── backend/          # Django project settings & URL configuration
│   ├── expenses/         # App with Expense, Budget, SavingsGoal models & views
│   │   ├── ml_model.py   # Machine Learning prediction engine
│   │   ├── models.py     # Database schema definitions
│   │   ├── views.py      # REST APIs (CRUD, analytics, predictions, seed)
│   │   └── serializers.py# DRF Serializers
│   ├── manage.py
│   └── db.sqlite3        # Local SQLite database
├── frontend/
│   ├── src/
│   │   ├── App.jsx       # Complete fintech UI & views
│   │   ├── App.css       # Glassmorphism styling & animations
│   │   ├── index.css     # Design tokens & color system
│   │   └── main.jsx
│   ├── index.html
│   └── package.json
└── run_project.bat       # One-click Windows launcher
```
