from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sqlite3
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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

class Inquiry(BaseModel):
    name: str
    email: str
    message: str

# Serve the HTML page directly when opening the root URL
@app.get("/")
def serve_home():
    return FileResponse("index.html")

@app.post("/inquiries")
def create_inquiry(item: Inquiry):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO inquiries (name, email, message) VALUES (?, ?, ?)", 
        (item.name, item.email, item.message)
    )
    conn.commit()
    conn.close()
    return {"status": "success"}

@app.get("/inquiries")
def get_inquiries():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, email, message FROM inquiries ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [{"name": r[0], "email": r[1], "message": r[2]} for r in rows]