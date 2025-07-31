
import os, shutil, tempfile, logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import List

from .models import init_db, SessionLocal, Upload
from .ingest import handle_upload

init_db()
app = FastAPI(title="BioWeave MVP")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename)[1].lower()
    if suffix not in (".csv", ".xlsx", ".xls"):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        record = handle_upload(tmp_path)
        return {"upload_id": record.id, "status": record.status}
    except Exception as exc:
        logging.exception("Processing failed")
        raise HTTPException(status_code=500, detail=str(exc))
    finally:
        os.remove(tmp_path)

@app.get("/uploads", response_model=List[dict])
def list_uploads():
    session = SessionLocal()
    items = session.query(Upload).order_by(Upload.created_at.desc()).all()
    data = [
        {
            "id": u.id,
            "filename": u.filename,
            "status": u.status,
            "created_at": u.created_at,
        }
        for u in items
    ]
    session.close()
    return data

@app.get("/uploads/{upload_id}")
def get_upload(upload_id: int):
    session = SessionLocal()
    u = session.get(Upload, upload_id)
    if not u:
        raise HTTPException(status_code=404, detail="Not found")
    session.close()
    return {
        "id": u.id,
        "filename": u.filename,
        "status": u.status,
        "report": u.report,
        "dataset_path": u.dataset_path,
    }
