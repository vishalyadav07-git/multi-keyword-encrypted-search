# 🔐 Multi-Keyword Ranked Search over Encrypted Data

A secure document search system that allows users to search encrypted documents using multiple keywords without storing the document content in plaintext.

The project uses Python, FastAPI, PostgreSQL, Fernet encryption, HMAC-SHA256 keyword hashing, and a TF-IDF-inspired ranking mechanism.

---

## 📌 Project Overview

Traditional search systems usually store documents and their searchable keywords in plaintext.

This creates a security problem because sensitive documents and search-related information may be exposed if the database is compromised.

This project addresses that problem by:

- Encrypting document content before storing it.
- Converting searchable keywords into HMAC-SHA256 hashes.
- Storing keyword frequencies instead of plaintext keywords.
- Supporting multiple keyword searches.
- Supporting AND and OR search modes.
- Ranking matching documents based on relevance.
- Decrypting document content only when an authorized retrieval request is made.

---

## 🎯 Objectives

The main objectives of this project are:

1. Securely store sensitive documents.
2. Prevent plaintext document content from being stored in the database.
3. Protect searchable keywords using cryptographic hashing.
4. Support multi-keyword search.
5. Provide AND and OR search operations.
6. Rank search results according to relevance.
7. Provide CRUD operations for documents.
8. Provide a simple web-based interface.

---

## 🏗️ System Architecture

```text
                    USER
                     │
                     ▼
              HTML/CSS/JavaScript
                     │
                     ▼
                  FastAPI
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
    Encryption   Keyword       Search
                  Indexing
        │            │            │
        │            ▼            ▼
        │       HMAC-SHA256    Ranking
        │                          │
        └────────────┬─────────────┘
                     ▼
                PostgreSQL

## 1. Problem Statement

When documents are stored in the cloud, searching them can expose sensitive information if document contents and searchable keywords are stored in plaintext.

The goal of this project is to explore a privacy-preserving search mechanism that allows users to search documents using multiple keywords while keeping document contents encrypted in storage.

## 2. How the Project Works

1. **Document upload:** The user submits a document to the application.
2. **Encryption:** The document content is encrypted before it is stored in the database.
3. **Keyword indexing:** Searchable keywords are processed using HMAC-SHA256 to create protected keyword indexes.
4. **Multi-keyword search:** The user searches using multiple keywords with AND or OR matching.
5. **Ranking:** Matching documents are ordered by relevance.
6. **Document retrieval:** The application retrieves and decrypts document content when requested.

## 3. Technologies Used

- **Python:** Backend programming.
- **FastAPI:** REST API development.
- **PostgreSQL:** Storage for document records and indexes.
- **SQLAlchemy:** Database interaction.
- **Fernet encryption:** Protects document content.
- **HMAC-SHA256:** Creates keyed keyword hashes.
- **HTML, CSS, and JavaScript:** User interface.
- **Uvicorn:** Runs the FastAPI application.

## 4. Setup Instructions

### Prerequisites

- Python
- PostgreSQL
- Git

### Step 1: Clone the repository

```bash
git clone https://github.com/vishalyadav07-git/multi-keyword-encrypted-search.git
cd multi-keyword-encrypted-search
```

### Step 2: Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### Step 3: Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 4: Configure environment variables

Create a local `.env` file based on `.env.example`. Configure the database URL and any encryption or search keys required by the application.

Never upload your actual `.env` file or secret keys to GitHub.

### Step 5: Run the application

Use the entry point configured in your project. For example, if your FastAPI instance is in `app/main.py`:

```bash
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` to explore the API, if Swagger documentation is enabled.
