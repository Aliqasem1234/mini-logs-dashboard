# Mini Logs Dashboard
A lightweight, real-time logging system built with PostgreSQL, Python, and Streamlit.

## 🌟 Highlights
- Self-registration & role-based login (viewer / admin)
- Insert logs (INFO, WARNING, ERROR) via web form or REST API
- Real-time table updates, Excel export & 24-hour timeline chart
- Audio alert on ERROR (admin only)
- Clean code, ready for Streamlit Cloud or Docker

## 📸 Screenshot
![Dashboard](https://i.imgur.com/placeholder.png)
*(replace with your own screenshot)*

## 🚀 Quick Start
1. Clone & enter folder
   ```bash
   git clone https://github.com/YOUR_USERNAME/mini-logs-dashboard.git
   cd mini-logs-dashboard


2.Install dependencies
pip install -r requirements.txt



3.Create PostgreSQL DB & tables
CREATE DATABASE logs;
CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT NOW(),
    level VARCHAR(10),
    service VARCHAR(50),
    message TEXT,
    context JSONB
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'viewer'
);

-- first admin (password = 123)
INSERT INTO users (username, password_hash, role)
VALUES ('admin', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'admin');



4.Update db_config.py with your credentials.



Run Streamlit
streamlit run app.py --server.port 8501
Open http://localhost:8501



6.Run FastAPI (optional)
Docs: http://127.0.0.1:8000/docs

📊 API Example
curl "http://127.0.0.1:8000/logs?page=1&size=5&level=ERROR"


📁 File Structure

mini-logs-dashboard/
├── app.py              # Streamlit UI + login + export
├── api.py              # FastAPI REST endpoints
├── auth.py             # SHA-256 password utils
├── db_config.py        # PostgreSQL credentials
├── fetch_logs.py       # Pagination & filters
├── insert_log.py       # Insert function
├── requirements.txt    # Python packages
└── README.md           # This file

🛠️ Tech Stack
Backend: Python 3.11+, PostgreSQL, FastAPI
Frontend: Streamlit, Pandas, ExcelWriter
Auth: SHA-256 hashing, session state
Charts: Native Streamlit + Altair timeline
🚦 Roadmap
Docker image
OAuth login (Google/GitHub)
Slack/Teams webhooks on ERROR
Dark mode toggle
🤝 Contributing
Pull requests are welcome!
Fork the repo
Create your feature branch (git checkout -b feature/amazing)
Commit your changes (git commit -m 'Add amazing feature')
Push to the branch (git push origin feature/amazing)
Open a Pull Request
📄 License
MIT – feel free to use in personal or commercial projects.
✨ Author
Ali Alsalaima – aliqasem606060@gmail.com
