import openai
import os
from fastapi import FastAPI, HTTPException
from typing import Dict, List
import requests

app = FastAPI()

# Debugging - Print script location
print(f"Running main.py from: {os.path.abspath(__file__)}")

# Mock Data
mock_users = {
    "admin_user": {"name": "Admin User", "role": "Administrator", "status": "Active"},
    "jdoe": {"name": "John Doe", "role": "Developer", "status": "Active"},
}

mock_hosts = {
    "host-001": {"hostname": "host-001", "os": "Windows 10", "owner": "jdoe", "last_seen": "2025-03-20"},
    "host-002": {"hostname": "host-002", "os": "Ubuntu 22.04", "owner": "admin_user", "last_seen": "2025-03-22"},
}

mock_alerts = [
    {"alert_id": "A123", "user": "admin_user", "host": "host-002", "event": "Suspicious program installed"},
    {"alert_id": "A124", "user": "jdoe", "host": "host-001", "event": "Failed login attempt"},
]

# Root Endpoint
@app.get("/")
def read_root():
    return {"message": "FastAPI POC Mock is running!"}

# Correlate User Data
@app.get("/correlate/{username}")
def correlate_user_activity(username: str):
    user_info = mock_users.get(username, None)
    if not user_info:
        raise HTTPException(status_code=404, detail="User not found")

    user_hosts = [h for h in mock_hosts.values() if h["owner"] == username]
    user_alerts = [a for a in mock_alerts if a["user"] == username]

    return {
        "user_info": user_info,
        "user_hosts": user_hosts,
        "user_alerts": user_alerts,
    }

# ✅ GPT-Powered Querying for Analysts (Supports GET & POST)
@app.post("/query")
@app.get("/query")
def query_gpt(user_query: Dict[str, str] = {"query": ""}):
    query_text = user_query.get("query", "").strip()

    if not query_text:
        raise HTTPException(status_code=400, detail="Query is empty")

    # Example: Check for user-related queries
    if "alerts for" in query_text.lower():
        username = query_text.lower().split("alerts for")[-1].strip()
        response = correlate_user_activity(username)
    else:
        response = {"message": "Query type not recognized"}

    # GPT Formatting (Mock Output)
    gpt_response = f"Security Report:\n{response}"
    
    return {"gpt_output": gpt_response}

# ✅ Debugging
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080, reload=True)
