from fastapi import FastAPI

app = FastAPI()

records = []

@app.get("/health")
async def health():
  return {"status": "ok"}

@app.get("/records")
async def get_records():
  return records
