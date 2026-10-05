from models import Author


def save_row(db, row):
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def find_author(db, name):
    return db.query(Author).filter(Author.name == name).first()


def ingest_voice_webhook(db, payload):
    pass
