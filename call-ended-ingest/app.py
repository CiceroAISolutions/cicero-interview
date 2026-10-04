from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from db import get_db, init_db
from models import Author

init_db()
app = FastAPI()


@app.get("/authors")
def list_authors(db: Session = Depends(get_db)):
    return [{"id": author.id, "name": author.name} for author in db.query(Author).all()]


@app.post("/webhooks/voice")
def voice_webhook(payload: dict, db: Session = Depends(get_db)):
    raise HTTPException(status_code=501, detail="Implement ingest")
