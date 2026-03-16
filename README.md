# AI Journal API

A FastAPI-based AI-powered journaling backend that allows users to create personal journal entries and automatically analyze them using Large Language Models (LLMs).

Each journal entry is processed using Groq's Llama 3.3 70B model, enabling intelligent sentiment detection, keyword extraction, summarization, and mood scoring.

The API also generates a weekly emotional trend report based on the user's journal history.

This project demonstrates how to combine:

- FastAPI for building modern APIs
- SQLAlchemy for database ORM
- JWT Authentication for secure login
- Groq LLM (Llama 3.3 70B) for intelligent journal analysis


--------------------------------------------------

FEATURES

User Authentication

- User signup with email and password
- Secure password hashing using bcrypt
- JWT-based authentication
- OAuth2 password flow login


--------------------------------------------------

AI JOURNAL ANALYSIS

Each journal entry is analyzed using a Groq-powered LLM pipeline that extracts:

- Sentiment classification (Positive / Neutral / Negative)
- Mood score (0–10 emotional scale)
- Keyword extraction
- Intelligent summary generation
- Timestamp recording

This replaces traditional rule-based NLP with LLM-based semantic understanding.


--------------------------------------------------

JOURNAL MANAGEMENT

Users can:

- Create new journal entries
- View all their entries
- View a specific journal entry
- Access a weekly mood report


--------------------------------------------------

WEEKLY MOOD ANALYTICS

The API analyzes journal entries from the last 7 days and returns:

- Total journal entries
- Positive mood days
- Neutral mood days
- Negative mood days
- Overall emotional trend


--------------------------------------------------

TECH STACK

Technology: Purpose

FastAPI — Backend API framework  
SQLAlchemy — ORM for database interaction  
SQLite — Local database  
JWT (python-jose) — Authentication  
Passlib (bcrypt) — Password hashing  
Groq API — LLM inference  
Llama 3.3 70B — Journal analysis model  
Pydantic — Data validation
Sentence Transformers — Text embedding model
ChromaDB — Vector database for semantic search

--------------------------------------------------

PROJECT STRUCTURE

AI-Journal-API

main.py  
journal.db  
requirements.txt  
.env  
README.md


--------------------------------------------------

INSTALLATION

1. Clone the repository

git clone https://github.com/your-username/ai-journal-api.git
cd ai-journal-api


--------------------------------------------------

2. Create virtual environment

python -m venv venv


Activate it

Windows

venv\Scripts\activate


Mac/Linux

source venv/bin/activate


--------------------------------------------------

3. Install dependencies

pip install fastapi uvicorn sqlalchemy passlib[bcrypt] python-jose groq python-dotenv sentence-transformers chromadb


--------------------------------------------------

4. Configure Environment Variables

Create a .env file in the root directory.

GROQ_API_KEY=your_groq_api_key_here  
SECRET_KEY=your_secret_key  
ALGORITHM=HS256  
ACCESS_TOKEN_EXPIRE_MINUTES=30

Using environment variables ensures secure API key management.


--------------------------------------------------

5. Run the server

uvicorn main:app --reload


Server runs at:

http://127.0.0.1:8000


Interactive API docs:

http://127.0.0.1:8000/docs


--------------------------------------------------

API ENDPOINTS


ROOT

GET /

Returns API status.

Response

{
  "message": "AI-JOURNAL-API is running"
}


--------------------------------------------------

AUTHENTICATION


Signup

POST /signup

Create a new user.

Request Body

{
  "email": "user@example.com",
  "password": "securepassword"
}

Response

{
  "message": "User created successfully",
  "email": "user@example.com"
}


--------------------------------------------------

Login

POST /login

Uses OAuth2 password flow.

Form Data

username: user@example.com  
password: securepassword

Response

{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer"
}

Use token in headers:

Authorization: Bearer <token>


--------------------------------------------------

JOURNAL ENDPOINTS


Create Journal Entry

POST /journal

Creates a journal entry and performs LLM-based analysis.

Request Body

{
  "content": "Today I felt productive and completed my project."
}

Response

{
  "message": "new journal created successfully"
}

The LLM automatically extracts:

- Sentiment
- Mood score
- Keywords
- Summary


--------------------------------------------------

Get All Entries

GET /entries

Returns all journal entries for the logged-in user.

Example Response

[
  {
    "id": 1,
    "content": "Today was a productive day",
    "sentiment": "Positive",
    "mood_score": 8,
    "keywords": "project, productivity",
    "summary": "Completed an important project and felt productive.",
    "created_at": "2026-03-15"
  }
]


--------------------------------------------------

Get Specific Entry

GET /entries/{id}

Returns a specific journal entry.

Security check ensures users can only access their own entries.

Example

GET /entries/1


Response

{
  "content": "Today I studied FastAPI",
  "sentiment": "Positive",
  "mood_score": 7,
  "keywords": "fastapi, learning",
  "summary": "Studied FastAPI and explored backend API development.",
  "created_at": "2026-03-15"
}


--------------------------------------------------

WEEKLY MOOD REPORT

GET /weeklyreport

Analyzes journal entries from the last 7 days.

Example Response

{
  "total_entries": 5,
  "positive_days": 3,
  "neutral_days": 1,
  "negative_days": 1
}

This provides a quick overview of the user's emotional trends.


--------------------------------------------------

SEMANTIC SEARCH

GET /search

Search journal entries by meaning, not just keywords.

Example

GET /search?query=feeling stressed about money

Response

{
  "results": [
    {
      "id": 7,
      "content": "Stressed about the payment of a loan",
      "sentiment": "Negative",
      "summary": "The person is feeling stressed about an upcoming loan payment."
    }
  ]
}

Uses sentence embeddings and ChromaDB vector database to find semantically similar entries. 
Searching "received my salary" returns payment and finance related entries even with zero exact word matches.

--------------------------------------------------

AI PROCESSING PIPELINE


Sentiment Analysis

The Groq LLM classifies journal entries into:

- Positive
- Neutral
- Negative


--------------------------------------------------

Mood Score

Each entry receives a mood score from 0–10.

Score interpretation:

0–3 → Negative  
4–6 → Neutral  
7–10 → Positive


--------------------------------------------------

Keyword Extraction

Important topics and concepts are extracted from the journal entry.

Example

Input

"I worked on my AI project and learned FastAPI today."

Keywords

AI project, FastAPI


--------------------------------------------------

Intelligent Summary

The LLM generates a concise summary of the journal entry using semantic understanding.


--------------------------------------------------

SECURITY

The API implements several security best practices:

- bcrypt password hashing
- JWT authentication
- Environment variables for secret management
- User ownership validation for journal entries

Users cannot access journals belonging to other users.


--------------------------------------------------

FUTURE IMPROVEMENTS

Possible enhancements:

- Emotion trend visualization graphs
- Monthly mood analytics
- LLM-powered journaling insights
- Frontend dashboard
- PostgreSQL production database
- Async FastAPI endpoints
- Docker deployment
- Vector search for journal retrieval
- Persistent PostgreSQL vector storage
- Multi-language semantic search


--------------------------------------------------

LEARNING OUTCOMES

This project demonstrates practical implementation of:

- REST API development
- Authentication systems
- SQLAlchemy ORM relationships
- LLM integration in backend applications
- Secure environment variable management
- AI-assisted personal analytics


--------------------------------------------------

LICENSE

This project is open source and available for educational and personal use.


--------------------------------------------------

AUTHOR

Developed as a backend project exploring AI-assisted journaling and LLM-powered emotional analytics using FastAPI and Groq.