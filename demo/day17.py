from fastapi import FastAPI, status, Depends
from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated

app = FastAPI()

records = []

class RecordCreate(BaseModel):
  model_config = ConfigDict(str_strip_whitespace=True)
  topic: str = Field(min_length=1)
  hours: float = Field(ge=0, le=24, strict=True)

class RecordResponse(BaseModel):
  topic: str
  hours: float
  id: int

class RecordRepository:
  def __init__(self):
    self.records: list[RecordResponse] = []
    self.next_id = 1
  
  def create(self, record: RecordCreate) -> RecordResponse:
    created = RecordResponse(id=self.next_id, topic=record.topic, hours=record.hours)
    self.records.append(created)
    self.next_id += 1
    return created
  
  def list_all(self) -> list[RecordResponse]:
    return self.records

record_repository = RecordRepository()

def get_repository() -> RecordRepository:
  return record_repository

@app.get("/health")
async def health():
  return {"status": "ok"}

@app.get("/records", response_model=list[RecordResponse])
async def get_records(store: Annotated[RecordRepository, Depends(get_repository)]):
  return store.list_all()

@app.post("/records/validate", response_model=RecordCreate)
async def validate_records(record: RecordCreate):
  return record

@app.post(
  "/records",
  response_model=RecordResponse,
  status_code=status.HTTP_201_CREATED,
)
async def create_records(
  record: RecordCreate,
  store: Annotated[RecordRepository, Depends(get_repository)],
):
  return store.create(record)