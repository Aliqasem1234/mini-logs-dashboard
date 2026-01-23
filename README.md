# Mini Logs Dashboard

A lightweight internal logging system built with **Python**, **Streamlit**, **FastAPI**, and **PostgreSQL (Supabase)**.

The project combines a web-based dashboard for users and administrators with a REST API for programmatic access to logs.

---

## 🌟 Highlights

- User self-registration and secure login
- Role-based access control (viewer / admin)
- Users can only view their own logs
- Admins can view and manage all logs
- Log levels: INFO, WARNING, ERROR
- JSON context support (stored as JSONB)
- Interactive 24-hour timeline visualization
- Export logs to Excel
- Manual refresh button
- REST API built with FastAPI
- Secure environment-based configuration (.env / Streamlit Secrets)
- Runs locally and in production (Streamlit Cloud)

---

## 🖥️ Components

- **Streamlit Dashboard**
  - User interface
  - Authentication
  - Log creation
  - Visualization & export

- **FastAPI Backend**
  - REST endpoints for logs
  - Pagination and filtering
  - Shared database with Streamlit

---

## 🚀 Quick Start (Local Setup)

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/mini-logs-dashboard.git
cd mini-logs-dashboard.

#------------------------------------------------#

2. Install dependencies
pip install -r requirements.txt

3. Create PostgreSQL tables
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'viewer'
);

CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT NOW(),
    level VARCHAR(10),
    service VARCHAR(50),
    message TEXT,
    context JSONB,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);

4. Create .env file (local only)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD="your_password"


⚠️ .env must not be committed to GitHub.

▶️ Run Streamlit Dashboard
streamlit run app.py


Open:

http://localhost:8501

▶️ Run FastAPI (optional)
uvicorn api:app --reload


API documentation:

http://127.0.0.1:8000/docs

📁 Project Structure
mini-logs-dashboard/
├── app.py              # Streamlit dashboard
├── api.py              # FastAPI REST API
├── auth.py             # Authentication logic
├── insert_log.py       # Log insertion
├── fetch_logs.py       # Role-based queries
├── db_config.py        # Database configuration
├── requirements.txt
├── README.md

🛠️ Tech Stack

Backend: Python, FastAPI

Frontend: Streamlit

Database: PostgreSQL (Supabase)

Driver: psycopg

Data: pandas

Export: Excel (xlsxwriter)

Auth: SHA-256 hashing

🚦 Roadmap

API authentication (token-based)

Log filtering via UI

Pagination controls

Docker support

OAuth login (GitHub / Google)

📄 License

MIT License – free to use for personal and commercial projects.

✨ Author

Developed by Ali Alsalaima
Email: aliqasem606060@gmail.com