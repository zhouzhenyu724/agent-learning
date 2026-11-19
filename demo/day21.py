from sqlite3 import Cursor
from contextlib import closing
from fastapi import FastAPI, Depends, status, HTTPException, Response
from typing import Annotated, Iterator
from contextlib import asynccontextmanager
from pydantic import BaseModel, Field, ConfigDict
import sqlite3
from pathlib import Path
import os
from fastapi.middleware.cors import CORSMiddleware

DB_PATH = Path(
    os.getenv("DAY21_DB_PATH") or Path(__file__).with_name("day21.sqlite3")
)

configured_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173")

allowed_origins = [
    origin.strip() for origin in configured_origins.split(",") if origin.strip()
]

class RecordCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    topic: str = Field(min_length=1)
    hours: float = Field(ge=0, le=24, strict=True)

class RecordUpdate(BaseModel):
  model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
  topic: str | None = Field(default=None, min_length=1)
  hours: float | None = Field(default=None, ge=0, le=24, strict=True)

class RecordResponse(BaseModel):
    topic: str
    hours: float
    id: int


@asynccontextmanager
async def lifespan(app: FastAPI):
  with closing(sqlite3.connect(DB_PATH)) as db, db:
    db.execute("""
      CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT NOT NULL CHECK (length(trim(topic)) > 0),
        hours REAL NOT NULL CHECK (hours BETWEEN 0 AND 24)
      )
    """)
  yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Content-Type"],
)

def get_db() -> Iterator[sqlite3.Connection]:
  with closing(sqlite3.connect(DB_PATH, check_same_thread=False)) as db:
    db.row_factory = sqlite3.Row
    yield db

Database = Annotated[sqlite3.Connection, Depends(get_db)]


def require_record(row: sqlite3.Row | None) -> dict:
    if row is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return dict(row)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/records", response_model=list[RecordResponse])
def get_records(db: Database, topic: str | None = None):
  rows = db.execute("SELECT id, topic, hours FROM records WHERE (? IS NULL OR topic = ?) ORDER BY id", (topic, topic)).fetchall()
  return [dict(row) for row in rows]

@app.get("/records/{record_id}", response_model=RecordResponse)
def get_record(record_id: int, db: Database):
  with db, closing[Cursor](db.execute("SELECT id, topic, hours FROM records WHERE id = ?", (record_id,))) as cursor:
    return require_record(cursor.fetchone())

@app.post("/records", response_model=RecordResponse, status_code=status.HTTP_201_CREATED)
def create_record(record: RecordCreate, db: Database):
  with db, closing[Cursor](db.execute("INSERT INTO records (topic, hours) VALUES (?, ?) RETURNING id, topic, hours", (record.topic, record.hours))) as cursor:
    return require_record(cursor.fetchone())

@app.post("/records/validate", response_model=RecordCreate)
def validate_record(record: RecordCreate):
    return record

@app.patch("/records/{record_id}", response_model=RecordResponse)
def update_record(record_id: int, record: RecordUpdate, db: Database):
  changes = record.model_dump(exclude_unset=True)
  if not changes or any(value is None for value in changes.values()):
    raise HTTPException(status_code=422, detail="至少提供一个字段，字段值不能为 null")
  with db, closing[Cursor](db.execute("UPDATE records SET topic = COALESCE(?, topic), hours = COALESCE(?, hours) WHERE id = ? RETURNING id, topic, hours", (changes.get("topic"), changes.get("hours"), record_id))) as cursor:
    return require_record(cursor.fetchone())

@app.delete("/records/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_record(record_id: int, db: Database):
  with db, closing[Cursor](db.execute("DELETE FROM records WHERE id = ?", (record_id,))) as cursor:
    if cursor.rowcount == 0:
      raise HTTPException(status_code=404, detail="Record not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)