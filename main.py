from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Allow the frontend browser page to talk to this server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Initialize the SQLite database table on startup
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Data schema for incoming submissions
class Inquiry(BaseModel):
    name: str
    email: str
    message: str

# 2. API Endpoint to receive and save submissions
@app.post("/inquiries")
def create_inquiry(item: Inquiry):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO inquiries (name, email, message) VALUES (?, ?, ?)", 
                   (item.name, item.email, item.message))
    conn.commit()
    conn.close()
    return {"status": "success"}

# 3. API Endpoint to return all saved records
@app.get("/inquiries")
def get_inquiries():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, email, message FROM inquiries ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [{"name": r[0], "email": r[1], "message": r[2]} for r in rows]