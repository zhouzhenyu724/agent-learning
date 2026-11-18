from fastapi import FastAPI, Depends, status, HTTPException
from typing import Annotated
from pydantic import BaseModel, Field, ConfigDict

app = FastAPI()

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
    
    def get_by_id(self, record_id: int) -> RecordResponse:
      for record in self.records:
        if record.id == record_id:
          return record
      raise HTTPException(status_code=404, detail="Record not found")
      
    
    def list_all(self) -> list[RecordResponse]:
      return self.records.copy()

record_repository = RecordRepository()

def get_repository() -> RecordRepository:
  return record_repository

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/records", response_model=list[RecordResponse])
async def get_records(store: Annotated[RecordRepository, Depends(get_repository)], topic: str | None = None):
  records = store.list_all()
  if topic is None:
    return records
  return [record for record in records if record.topic == topic]

@app.get("/records/{record_id}", response_model=RecordResponse)
async def get_record(record_id: int, store: Annotated[RecordRepository, Depends(get_repository)]):
    return store.get_by_id(record_id)

@app.post("/records", response_model=RecordResponse, status_code=status.HTTP_201_CREATED)
async def create_record(
  record: RecordCreate,
  store: Annotated[RecordRepository, Depends(get_repository)],
):
    return store.create(record)

@app.post("/records/validate", response_model=RecordCreate)
async def validate_record(record: RecordCreate):
    return record