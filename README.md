# Mini Logs Dashboard
A lightweight real-time logging system built with PostgreSQL, Python and Streamlit.

## Features
- Insert logs (INFO, WARNING, ERROR) through a web form
- View latest logs in an interactive table
- Bar-chart summary by log level
- Optional JSON context field

## Quick Start
1. Clone the repo
   ```bash
   git clone https://github.com/Aliqasem1234/mini-logs-dashboard.git
   cd mini-logs-dashboard


2.Install dependencies
pip install -r requirements.txt

3.Create PostgreSQL database & table

CREATE DATABASE mini_logs;
CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT NOW(),
    level VARCHAR(10),
    service VARCHAR(50),
    message TEXT,
    context JSONB
);

4.Update db_config.py with your credentials

5.Run the app
streamlit run app.py

6.Open http://localhost:8501 in your browser


File Structure
mini-logs-dashboard/
├── app.py              # Streamlit UI
├── db_config.py        # DB credentials
├── insert_log.py       # Insert function
├── fetch_logs.py       # Query function
├── requirements.txt    # Python packages
└── README.md           # This file