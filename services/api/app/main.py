from fastapi import FastAPI, Depends
from pydantic import BaseModel
from .db import init_db, SessionLocal
from sqlalchemy.orm import Session
from .models import JobResult
from .kafka_producer import send_job, KafkaProducerSingleton

app = FastAPI(title="FastAPI + Kafka + Celery + MySQL")

class JobIn(BaseModel):
    text: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def on_startup():
    init_db()

@app.on_event("shutdown")
async def on_shutdown():
    await KafkaProducerSingleton.close()

@app.get("/")
def health():
    return {"ok": True}

@app.post("/submit")
async def submit_job(job: JobIn, db: Session = Depends(get_db)):
    # DB에 PENDING 레코드 생성
    row = JobResult(input_text=job.text, status="QUEUED")
    db.add(row)
    db.commit()
    db.refresh(row)

    # Kafka 로 메시지 발행
    await send_job({"id": row.id, "text": job.text})
    return {"id": row.id, "status": "QUEUED"}

@app.get("/results/{job_id}")
def get_result(job_id: int, db: Session = Depends(get_db)):
    row = db.get(JobResult, job_id)
    if not row:
        return {"error": "not found"}
    return {"id": row.id, "status": row.status, "note": row.note, "input_text": row.input_text}
