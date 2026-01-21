# api.py
from fastapi import FastAPI, Query
from fetch_logs import hamta_loggar, rakna_loggar
import pandas as pd

    


app = FastAPI(title="Mini Logs API")

@app.get("/")
def root():
    return {"message": "Mini Logs API – go to /docs"}

@app.get("/logs")
def get_logs(page: int = Query(1, ge=1),
             size: int = Query(50, ge=1, le=500),
             level: str = Query(None, regex="^(INFO|WARNING|ERROR)$")):
    df = hamta_loggar(sida=page, antal_per_sida=size, level_filter=level)
    total = rakna_loggar(level_filter=level)
    return {
        "total": total,
        "page": page,
        "size": len(df),
        "data": df.to_dict(orient="records")
    }