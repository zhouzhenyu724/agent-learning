from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI()

records = []

class RecordCreate(BaseModel):
  model_config = ConfigDict(str_strip_whitespace=True)
  topic: str = Field(min_length=1)
  hours: float = Field(ge=0, le=24, strict=True)


class RecordResponse(BaseModel):
  topic: str
  hours: float

@app.get("/health")
async def health():
  return {"status": "ok"}

@app.get("/records", response_model=list[RecordResponse])
async def get_records():
  return records

@app.post("/records/validate", response_model=RecordResponse)
async def validate_records(record: RecordCreate):
  return record