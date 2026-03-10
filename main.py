from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json, asyncio, os

app = FastAPI()

# Enable CORS so other devices (phones/friends) can connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "users.json"

# Create a database file if it doesn't exist
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({"admin": "hari123"}, f)

class UserAuth(BaseModel):
    username: str
    password: str

@app.get("/")
async def get_index():
    with open("index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.post("/signup")
async def signup(user: UserAuth):
    with open(DB_FILE, "r+") as f:
        data = json.load(f)
        if user.username in data:
            raise HTTPException(status_code=400, detail="User already exists")
        data[user.username] = user.password
        f.seek(0)
        json.dump(data, f)
    return {"message": "Account Created"}

@app.post("/login")
async def login(user: UserAuth):
    with open(DB_FILE, "r") as f:
        data = json.load(f)
        if data.get(user.username) == user.password:
            return {"message": "Success"}
    raise HTTPException(status_code=401, detail="Invalid Credentials")

@app.websocket("/ws/data")
async def data_stream(websocket: WebSocket):
    await websocket.accept()
    while True:
        # Heartbeat to keep the connection alive
        await websocket.send_text(json.dumps({"status": "live"}))
        await asyncio.sleep(1)

if __name__ == "__main__":
    import uvicorn
    # Use 0.0.0.0 to allow external device access
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)