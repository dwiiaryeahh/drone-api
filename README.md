# Drone Info API

FastAPI application for managing drone device information.

## Database
- **Database name**: drone_info.db (SQLite)
- **Table name**: info
- **Schema**: 
  - id (INTEGER, PRIMARY KEY, AUTOINCREMENT)
  - device (TEXT) - Values: "drone_besar" or "drone_kecil"
  - status (BOOLEAN) - Values: true or false

## Installation

```bash
pip install -r requirements.txt
```

## Running the API

```bash
python main.py
```

The API will run on **http://localhost:1308**

## API Endpoints

### 1. Update Device Info
**POST** `/update`

Update or insert device status. If device exists, updates its status; otherwise creates a new entry.

**Request Body:**
```json
{
  "device": "drone_besar",
  "status": true
}
```

**Response:**
```json
{
  "id": 1,
  "device": "drone_besar",
  "status": true
}
```

### 2. Get Device Data
**GET** `/data`

Get all data from the info table.

**Response:**
```json
[
  {
    "id": 1,
    "device": "drone_besar",
    "status": true
  },
  {
    "id": 2,
    "device": "drone_kecil",
    "status": false
  }
]
```

## Interactive API Documentation

Once running, visit:
- Swagger UI: http://localhost:1308/docs
- ReDoc: http://localhost:1308/redoc
