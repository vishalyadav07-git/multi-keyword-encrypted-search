from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware #fe
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from .models import Base, Document , KeywordIndex
from .schemas import DocumentCreate, DocumentUpdate
from .encryption import encrypt_data, decrypt_data
from .search_index import (
    create_keyword_index,
    hash_keyword,
    extract_keywords
)
from sqlalchemy import func
import math

app = FastAPI()
#fe
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {
        "message": "Multi Keyword Ranked Search over Encrypted Data"
    }


@app.post("/documents")
def create_document(
    document: DocumentCreate,
    db: Session = Depends(get_db)
):
    # Encrypt document content
    encrypted_content = encrypt_data(document.content)

    # Create document
    new_document = Document(
        title=document.title,
        content=encrypted_content
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    # Create keyword index
    keyword_index = create_keyword_index(document.content)

    for item in keyword_index:

        new_keyword = KeywordIndex(
            document_id=new_document.id,
            keyword_hash=item["keyword_hash"],
            frequency=item["frequency"]
        )

        db.add(new_keyword)

    db.commit()

    return {
        "id": new_document.id,
        "message": "Document stored successfully"
    }

@app.get("/search")
def search_documents(
    query: str,
    mode: str = "OR",
    db: Session = Depends(get_db)
):

    # Process query exactly like document indexing
    keywords = extract_keywords(query)

    # Remove duplicate keywords
    keywords = list(dict.fromkeys(keywords))

    if not keywords:
        return {
            "query": query,
            "mode": mode,
            "results": []
        }

    mode = mode.upper()

    if mode not in ["AND", "OR"]:
        raise HTTPException(
        status_code=400,
        detail="Mode must be AND or OR"
    )

    total_documents = db.query(Document).count()

    if total_documents == 0:
        return {
            "query": query,
            "mode": mode,
            "results": []
        }

    results = {}

    for keyword in keywords:

        keyword_hash = hash_keyword(keyword)

        matches = (
            db.query(KeywordIndex)
            .filter(
                KeywordIndex.keyword_hash == keyword_hash
            )
            .all()
        )

        document_frequency = len(matches)

        if document_frequency == 0:
            continue

        # IDF
        idf = math.log(
            total_documents / document_frequency
        )

        for match in matches:

            document_id = match.document_id
            frequency = match.frequency

            # TF
            tf = frequency

            score = tf * idf

            if document_id not in results:

                results[document_id] = {
                    "score": 0,
                    "matched_keywords": 0
                }

            results[document_id]["score"] += score

            results[document_id]["matched_keywords"] += 1

    # AND search
    if mode == "AND":

        results = {
            document_id: data
            for document_id, data in results.items()
            if data["matched_keywords"] == len(keywords)
        }

    ranked_results = []

    for document_id, data in results.items():

        document = (
            db.query(Document)
            .filter(
                Document.id == document_id
            )
            .first()
        )

        if document:

            ranked_results.append({
                "document_id": document.id,
                "title": document.title,
                "score": round(data["score"], 4),
                "matched_keywords": data["matched_keywords"]
            })

    ranked_results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return {
        "query": query,
        "mode": mode,
        "results": ranked_results
    }

@app.get("/documents/{document_id}")
def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    decrypted_content = decrypt_data(document.content)

    return {
        "id": document.id,
        "title": document.title,
        "content": decrypted_content
    }

@app.put("/documents/{document_id}")
def update_document(
    document_id: int,
    document: DocumentUpdate,
    db: Session = Depends(get_db)
):
    existing_document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not existing_document:
        raise HTTPException(
        status_code=404,
        detail="Document not found"
    )

    # Encrypt the new content
    encrypted_content = encrypt_data(document.content)

    # Update document
    existing_document.title = document.title
    existing_document.content = encrypted_content

    # Delete old keyword index
    db.query(KeywordIndex).filter(
        KeywordIndex.document_id == document_id
    ).delete()

    # Create new keyword index
    keyword_index = create_keyword_index(document.content)

    # Insert new keyword index
    for item in keyword_index:

        new_keyword = KeywordIndex(
            document_id=document_id,
            keyword_hash=item["keyword_hash"],
            frequency=item["frequency"]
        )

        db.add(new_keyword)

    db.commit()

    return {
        "message": "Document updated successfully"
    }

@app.delete("/documents/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not document:
        raise HTTPException(
        status_code=404,
        detail="Document not found"
    )

    # Delete keyword index records
    db.query(KeywordIndex).filter(
        KeywordIndex.document_id == document_id
    ).delete()

    # Delete document
    db.delete(document)

    db.commit()

    return {
        "message": "Document deleted successfully"
    }