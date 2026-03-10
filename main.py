from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import json, os

app = FastAPI()
DB = "users.json"

@app.get("/")
async def home():
    with open("index.html", "r") as f: return HTMLResponse(f.read())

@app.post("/register")
async def reg(req: Request):
    data = await req.json()
    with open(DB, "r+") as f:
        users = json.load(f)
        users[data['username']] = data['password']
        f.seek(0); json.dump(users, f); f.truncate()
    return {"success": True}
