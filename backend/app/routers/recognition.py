import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.dataset import Dataset
from app.models.recognition import RecognitionRecord
from app.schemas.recognition import (
    RecognitionStartRequest,
    RecognitionResultResponse,
    VisualizationResponse,
)
from app.services.inference import run_inference
from app.services.preprocessing import preprocess_signal, generate_visualization

router = APIRouter()


@router.post("/start", response_model=RecognitionResultResponse)
async def start_recognition(req: RecognitionStartRequest, db: Session = Depends(get_db)):
    dataset = db.query(Dataset).filter(Dataset.id == req.dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    iq_data = preprocess_signal(dataset.file_path, dataset.format)
    result = run_inference(iq_data)

    record = RecognitionRecord(
        id=str(uuid.uuid4()),
        dataset_id=req.dataset_id,
        modulation=result["modulation"],
        confidence=result["confidence"],
        snr=result["snr"],
        symbol_rate=result.get("symbol_rate"),
        freq_offset=result.get("freq_offset"),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/{record_id}", response_model=RecognitionResultResponse)
async def get_recognition_result(record_id: str, db: Session = Depends(get_db)):
    record = db.query(RecognitionRecord).filter(RecognitionRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record


@router.get("/history", response_model=list[RecognitionResultResponse])
async def get_history(db: Session = Depends(get_db)):
    return db.query(RecognitionRecord).order_by(RecognitionRecord.created_at.desc()).all()


@router.get("/visualization/{dataset_id}", response_model=VisualizationResponse)
async def get_visualization(dataset_id: str, db: Session = Depends(get_db)):
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    iq_data = preprocess_signal(dataset.file_path, dataset.format)
    viz = generate_visualization(iq_data)
    return viz
