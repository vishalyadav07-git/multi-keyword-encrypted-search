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