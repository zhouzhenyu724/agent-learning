from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .day23_repository import Record, find_record

app = FastAPI()
engine = create_engine(
    "postgresql+psycopg2://127.0.0.1/agent_learning_day22_migration"
)


class RecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    topic: str
    hours: float


def get_db() -> Iterator[Session]:
    with Session(engine) as session:
        yield session


def get_current_user_id() -> int:
    return 1  # 本地练习用 Alice 模拟当前用户


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
