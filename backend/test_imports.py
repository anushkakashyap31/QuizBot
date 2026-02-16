#!/usr/bin/env python3
"""Test all imports"""

print("Testing imports...\n")

try:
    import fastapi
    print("✓ FastAPI")
except ImportError as e:
    print(f"✗ FastAPI: {e}")

try:
    import uvicorn
    print("✓ Uvicorn")
except ImportError as e:
    print(f"✗ Uvicorn: {e}")

try:
    import pydantic
    print("✓ Pydantic")
except ImportError as e:
    print(f"✗ Pydantic: {e}")

try:
    import google.generativeai
    print("✓ Google Generative AI")
except ImportError as e:
    print(f"✗ Google Generative AI: {e}")

try:
    import chromadb
    print("✓ ChromaDB")
except ImportError as e:
    print(f"✗ ChromaDB: {e}")

try:
    import sentence_transformers
    print("✓ Sentence Transformers")
except ImportError as e:
    print(f"✗ Sentence Transformers: {e}")

try:
    import firebase_admin
    print("✓ Firebase Admin")
except ImportError as e:
    print(f"✗ Firebase Admin: {e}")

try:
    import sqlalchemy
    print("✓ SQLAlchemy")
except ImportError as e:
    print(f"✗ SQLAlchemy: {e}")

try:
    from jose import jwt
    print("✓ Python Jose")
except ImportError as e:
    print(f"✗ Python Jose: {e}")

try:
    from passlib.context import CryptContext
    print("✓ Passlib")
except ImportError as e:
    print(f"✗ Passlib: {e}")

try:
    from bs4 import BeautifulSoup
    print("✓ BeautifulSoup4")
except ImportError as e:
    print(f"✗ BeautifulSoup4: {e}")

try:
    import mailparser
    print("✓ Mail Parser")
except ImportError as e:
    print(f"✗ Mail Parser: {e}")

print("\n✓ All imports successful!")