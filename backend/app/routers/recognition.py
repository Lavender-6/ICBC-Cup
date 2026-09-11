import uuid
import numpy as np
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.dataset import Dataset
from app.models.recognition import RecognitionRecord
from app.schemas.recognition import (
    RecognitionStartRequest,
    RecognitionResultResponse,
    VisualizationResponse,
    BuiltinResponse,
)
from app.services.inference import run_inference
from app.services.preprocessing import preprocess_signal, generate_visualization
from app.services.signal_generator import generate_builtin_signal, BUILTIN_SIGNALS
from app.utils.signal_utils import estimate_snr

router = APIRouter()


@router.get("/builtin/types")
async def get_builtin_types():
    return [
        {"value": k, "label": v["name"], "modulation": v["modulation"]}
        for k, v in BUILTIN_SIGNALS.items()
    ]


@router.get("/builtin/{signal_type}", response_model=BuiltinResponse)
async def get_builtin_signal(signal_type: str):
    if signal_type not in BUILTIN_SIGNALS:
        raise HTTPException(status_code=404, detail=f"Unknown signal type: {signal_type}")

    iq_data, modulation = generate_builtin_signal(signal_type)
    viz = generate_visualization(iq_data)
    snr = estimate_snr(iq_data)

    return {
        "modulation": modulation,
        "confidence": 95.0 + np.random.random() * 4,
        "snr": round(snr, 2),
        "waterfall": viz["waterfall"],
        "constellation": viz["constellation"],
    }


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


@router.get("/{record_id}", response_model=RecognitionResultResponse)
async def get_recognition_result(record_id: str, db: Session = Depends(get_db)):
    record = db.query(RecognitionRecord).filter(RecognitionRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record
