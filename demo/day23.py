from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from fastapi.responses import Response

from .day23_repository import Record, find_record, create_record, update_record, delete_record, find_all_records

app = FastAPI()
engine = create_engine(
    "postgresql+psycopg2://127.0.0.1/agent_learning_day22_migration"
)


Topic = Annotated[str, Field(min_length=1)]
Hours = Annotated[float, Field(ge=0, le=24, strict=True)]

class RecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    topic: str
    hours: float

class RecordCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    topic: Topic
    hours: Hours


class RecordUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    topic: Topic | None = None
    hours: Hours | None = None

def save_response(db: Session, record: Record) -> RecordResponse:
    response = RecordResponse.model_validate(record)
    db.commit()
    return response


def get_db() -> Iterator[Session]:
    with Session(engine) as session:
        yield session


def get_current_user_id() -> int:
    return 1  # 本地练习用 Alice 模拟当前用户

@app.get("/records", response_model=list[RecordResponse])
def get_records(
    db: Annotated[Session, Depends(get_db)],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> list[Record]:
    records = find_all_records(db, user_id=user_id)
    return records

@app.get("/records/{record_id}", response_model=RecordResponse)
def get_record(
    record_id: int,
    db: Annotated[Session, Depends(get_db)],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> Record:
    record = find_record(db, user_id=user_id, record_id=record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@app.post("/records", response_model=RecordResponse, status_code=201)
def post_record(
    payload: RecordCreate,
    db: Annotated[Session, Depends(get_db)],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> RecordResponse:
    record = create_record(db, user_id=user_id, topic=payload.topic, hours=payload.hours)
    return save_response(db, record)


@app.patch("/records/{record_id}", response_model=RecordResponse)
def patch_record(
    record_id: int,
    payload: RecordUpdate,
    db: Annotated[Session, Depends(get_db)],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> RecordResponse:
    changes = payload.model_dump(exclude_unset=True)
    if not changes or any(value is None for value in changes.values()):
        raise HTTPException(status_code=422, detail="至少提供一个字段，字段值不能为 null")

    record = update_record(db, user_id=user_id, record_id=record_id, changes=changes)
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return save_response(db, record)


@app.delete("/records/{record_id}", status_code=204)
def remove_record(
    record_id: int,
    db: Annotated[Session, Depends(get_db)],
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> Response:
    if not delete_record(db, user_id=user_id, record_id=record_id):
        raise HTTPException(status_code=404, detail="Record not found")
    db.commit()
    return Response(status_code=204)