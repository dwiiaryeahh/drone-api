from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from contextlib import contextmanager

app = FastAPI(title="Drone Info API")

DATABASE_NAME = "drone_info.db"

# Pydantic models
class InfoUpdate(BaseModel):
    device: str
    status: bool

class InfoResponse(BaseModel):
    id: int
    device: str
    status: bool

# Database context manager
@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# Initialize database
def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device TEXT NOT NULL,
                status BOOLEAN NOT NULL
            )
        """)
        conn.commit()

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

# Endpoint 1: Update table info
@app.post("/update", response_model=InfoResponse)
async def update_info(data: InfoUpdate):
    """
    Update or insert device status in the info table.
    If device exists, update its status. Otherwise, create new entry.
    """
    if data.device not in ["drone_besar", "drone_kecil"]:
        raise HTTPException(
            status_code=400, 
            detail="Device must be either 'drone_besar' or 'drone_kecil'"
        )
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Check if device exists
        cursor.execute("SELECT id FROM info WHERE device = ?", (data.device,))
        existing = cursor.fetchone()
        
        if existing:
            # Update existing record
            cursor.execute(
                "UPDATE info SET status = ? WHERE device = ?",
                (data.status, data.device)
            )
            record_id = existing[0]
        else:
            # Insert new record
            cursor.execute(
                "INSERT INTO info (device, status) VALUES (?, ?)",
                (data.device, data.status)
            )
            record_id = cursor.lastrowid
        
        conn.commit()
        
        # Fetch and return the updated/created record
        cursor.execute("SELECT id, device, status FROM info WHERE id = ?", (record_id,))
        row = cursor.fetchone()
        
        return InfoResponse(
            id=row["id"],
            device=row["device"],
            status=bool(row["status"])
        )

# Endpoint 2: Get data from table info
@app.get("/data")
async def get_data():
    """
    Get all data from info table.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, device, status FROM info")
        rows = cursor.fetchall()
        
        return [
            {
                "id": row["id"],
                "device": row["device"],
                "status": bool(row["status"])
            }
            for row in rows
        ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1308)
