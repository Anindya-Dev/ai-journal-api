# AI Journal API

A **FastAPI-based AI-powered journaling backend** that allows users to create personal journal entries and automatically analyze them using basic Natural Language Processing (NLP).

The API performs **sentiment analysis, keyword extraction, and summarization** for each journal entry and provides a **weekly mood report** based on the user's emotional trends.

This project demonstrates how to combine:

* **FastAPI** for building modern APIs
* **SQLAlchemy** for database ORM
* **JWT Authentication** for secure login
* **TextBlob NLP** for text analysis

---

# Features

### User Authentication

* User signup with email and password
* Secure password hashing using **bcrypt**
* JWT-based authentication
* OAuth2 password flow login

### Journal Entry Analysis

Each journal entry is automatically analyzed for:

* Sentiment (Positive / Neutral / Negative)
* Keywords extraction
* Automatic summary generation
* Timestamp recording

### Journal Management

Users can:

* Create new journal entries
* View all their entries
* View a specific journal entry
* Access a weekly mood report

### Weekly Mood Analytics

The API calculates emotional trends for the last **7 days** and returns:

* Total journal entries
* Positive mood days
* Neutral mood days
* Negative mood days

---

# Tech Stack

| Technology        | Purpose                      |
| ----------------- | ---------------------------- |
| FastAPI           | Backend API framework        |
| SQLAlchemy        | ORM for database interaction |
| SQLite            | Local database               |
| JWT (python-jose) | Authentication               |
| Passlib (bcrypt)  | Password hashing             |
| TextBlob          | NLP analysis                 |
| Pydantic          | Data validation              |

---

# Project Structure

```
AI-Journal-API
│
├── main.py
├── journal.db
├── requirements.txt
└── README.md
```

---

# Installation

### 1. Clone the repository

```
git clone https://github.com/your-username/ai-journal-api.git
cd ai-journal-api
```

---

### 2. Create virtual environment

```
python -m venv venv
```

Activate it:

Windows

```
venv\Scripts\activate
```

Mac/Linux

```
source venv/bin/activate
```

---

### 3. Install dependencies

```
pip install fastapi uvicorn sqlalchemy passlib[bcrypt] python-jose textblob
```

---

### 4. Run the server

```
uvicorn main:app --reload
```

Server will run at:

```
http://127.0.0.1:8000
```

Interactive API docs:

```
http://127.0.0.1:8000/docs
```

---

# API Endpoints

## Root

### GET /

Returns API status.

Response

```
{
  "message": "AI-JOURNAL-API is running"
}
```

---

# Authentication

## Signup

### POST /signup

Create a new user.

Request Body

```
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

Response

```
{
  "message": "User created successfully",
  "email": "user@example.com"
}
```

---

## Login

### POST /login

Uses **OAuth2 password flow**.

Form Data

```
username: user@example.com
password: securepassword
```

Response

```
{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer"
}
```

Use the token in headers:

```
Authorization: Bearer <token>
```

---

# Journal Endpoints

## Create Journal Entry

### POST /journal

Creates a journal entry and performs NLP analysis.

Request Body

```
{
  "content": "Today I felt productive and completed my project."
}
```

Response

```
{
  "message": "new journal created successfully"
}
```

The system automatically extracts:

* Sentiment
* Keywords
* Summary

---

## Get All Entries

### GET /entries

Returns all journal entries for the logged-in user.

Example Response

```
[
  {
    "id": 1,
    "content": "Today was a productive day",
    "sentiment": "Positive",
    "keywords": "project, work",
    "summary": "Today was a productive day",
    "created_at": "2026-03-15"
  }
]
```

---

## Get Specific Entry

### GET /entries/{id}

Returns a specific journal entry.

Security check ensures users **can only access their own entries**.

Example

```
GET /entries/1
```

Response

```
{
  "content": "Today I studied FastAPI",
  "sentiment": "Positive",
  "keywords": "fastapi, learning",
  "summary": "Today I studied FastAPI",
  "created_at": "2026-03-15"
}
```

---

# Weekly Mood Report

### GET /weeklyreport

Analyzes journal entries from the **last 7 days**.

Example Response

```
{
  "total_entries": 5,
  "positive_days": 3,
  "neutral_days": 1,
  "negative_days": 1
}
```

This provides a quick overview of the user's emotional trends.

---

# NLP Processing

The API uses **TextBlob** for simple natural language processing.

### Sentiment Analysis

Determines whether an entry is:

* Positive
* Neutral
* Negative

### Keyword Extraction

Extracts noun phrases to identify important topics.

Example:

```
"I worked on my AI project today"
```

Keywords:

```
AI project
```

### Summary

Currently extracts:

* First sentence
* Last sentence
* Total number of sentences

---

# Security

The API uses:

* **bcrypt password hashing**
* **JWT token authentication**
* **User ownership checks for journal entries**

Users cannot access journals that belong to other users.

---

# Future Improvements

Possible enhancements:

* LLM-powered journal summaries
* Emotion trend graphs
* Monthly mood analytics
* Frontend dashboard
* PostgreSQL production database
* Async FastAPI endpoints
* Deployment using Docker

---

# Learning Outcomes

This project demonstrates practical implementation of:

* REST API development
* Authentication systems
* Database ORM relationships
* Basic NLP integration
* Secure backend design

---

# License

This project is open source and available for educational and personal use.

---

# Author

Developed as a backend project exploring **AI-assisted journaling and sentiment analysis APIs using FastAPI**.
