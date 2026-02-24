# 🤖 QuizBot — AI-Powered Non-Profit Educational Assessment Platform for the Non-Profit Sector

---

## Problem Statement

Develop an interactive AI-driven educational bot for the Non-Profit domain. The application engages users in targeted assessments based on **Donor Emails**, evaluating their responses using a Large Language Model. Beyond simple scoring, the bot provides deep contextual explanations for incorrect answers, creating a personalized learning loop that bridges knowledge gaps and reinforces industry-specific concepts.

## Major Tools	

Python, Vector DB, LLM API

---

## Key Features

- **AI Quiz Generation** — Paste any donor email and instantly generate 3–10 context-aware multiple-choice questions using Google Gemini 1.5 Flash
- **Semantic Search** — ChromaDB stores email embeddings for intelligent similarity matching and context retrieval
- **Smart Evaluation** — AI evaluates answers and generates personalized explanations for every question
- **User Authentication** — Secure sign-up and login via Firebase Authentication
- **Progress Tracking** — Full quiz history, accuracy trends, and performance analytics
- **Analytics Dashboard** — Visual breakdown of scores, streaks, and improvement over time

---

## Architecture Overview

QuizBot follows a **3-Tier Client-Server Architecture**:

```
┌─────────────────────────────────────────────┐
│           Presentation Layer                 │
│     React 19 + Vite + Tailwind CSS           │
└─────────────────┬───────────────────────────┘
                  │  REST API (Axios)
┌─────────────────▼───────────────────────────┐
│         Business Logic Layer                 │
│   FastAPI (Python) — Auth, Quiz, Analytics   │
└──────┬──────────┬──────────┬────────────────┘
       │          │          │
┌──────▼──┐  ┌───▼────┐  ┌──▼───────────────┐
│ Firebase │  │ SQLite │  │    ChromaDB       │
│  Auth +  │  │  ORM   │  │  Vector Search    │
│ Real-DB  │  │        │  │  (384-dim embed.) │
└──────────┘  └────────┘  └──────────────────┘
                  ↕ Google Gemini 1.5 Flash API
```

---

## 🛠️ Tech Stack

### Frontend
| Technology | Purpose |
|---|---|
| **React 19** | UI framework |
| **Vite** | Build tool & dev server |
| **Tailwind CSS** | Utility-first styling |
| **Framer Motion** | Animations & transitions |
| **Zustand** | Global state management |
| **Axios** | HTTP client for API calls |

### Backend
| Technology | Purpose |
|---|---|
| **FastAPI (Python)** | REST API framework |
| **SQLAlchemy 2.0** | ORM for SQLite |
| **SQLite** | Local structured data store |
| **ChromaDB** | Vector database for email embeddings |
| **Sentence Transformers** (`all-MiniLM-L6-v2`) | 384-dim text embeddings |
| **python-jose** | JWT token generation & verification |
| **bcrypt** | Password hashing (via Firebase) |
| **Pydantic V2** | Request/response validation |

### AI & Cloud Services
| Technology | Purpose |
|---|---|
| **Google Gemini 1.5 Flash** | Quiz generation, answer evaluation, summarization |
| **Firebase Authentication** | User sign-up, login, ID token management |
| **Firebase Realtime Database** | Quiz history, user profiles, progress data |
| **Firebase Admin SDK** | Server-side Firebase access |

---

## 📁 Project Structure

```
QuizBot/
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── requirements.txt
│   ├── .env                     # Environment variables (not committed)
│   ├── firebase_credentials.json  # Firebase service account (not committed)
│   ├── routes/
│   │   ├── auth.py              # /api/auth/*
│   │   ├── quiz.py              # /api/quiz/*
│   │   └── analytics.py         # /api/analytics/*
│   ├── services/
│   │   ├── auth_service.py      # Token verification & user CRUD
│   │   ├── llm_service.py       # Gemini API + retry logic
│   │   ├── quiz_generator.py    # Quiz generation & evaluation
│   │   ├── vector_db.py         # ChromaDB store & search
│   │   └── analytics_service.py # History & progress queries
│   └── models/
│       └── database.py          # SQLAlchemy models
├── frontend/
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   ├── tailwind.config.js
│   └── src/
│       ├── App.jsx
│       ├── main.jsx
│       ├── store/
│       │   ├── authStore.js      # Zustand auth state
│       │   └── quizStore.js      # Zustand quiz state
│       ├── pages/
│       │   ├── Home.jsx
│       │   ├── Login.jsx
│       │   ├── Register.jsx
│       │   ├── Quiz.jsx
│       │   ├── Dashboard.jsx
│       │   ├── History.jsx
│       │   ├── Progress.jsx
│       │   └── About.jsx
│       └── components/
│           ├── EmailInput.jsx
│           ├── QuizInterface.jsx
│           ├── QuestionCard.jsx
│           └── ResultCard.jsx
├── QuizBot_Documents/           # HLD, SDD, and other project docs
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## 🔌 API Reference

**Base URL:** `http://localhost:8000`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/api/auth/login` | ❌ | Verify Firebase token, return JWT + user profile |
| `GET` | `/api/auth/me` | ✅ | Get current authenticated user |
| `POST` | `/api/quiz/generate` | ✅ | Generate quiz from a donor email |
| `POST` | `/api/quiz/evaluate` | ✅ | Submit answers and receive AI evaluation |
| `GET` | `/api/analytics/history` | ✅ | Fetch all past quiz records |
| `GET` | `/api/analytics/progress` | ✅ | Get progress trends and analytics |
| `GET` | `/api/analytics/stats` | ✅ | Get combined user stats |

---

## 🔒 Security

- Firebase Authentication handles all password hashing and credential storage
- Dual-token model: Firebase ID token (auth) + short-lived JWT (API access, 1hr expiry)
- JWT verified on every protected API request (stateless backend)
- CORS restricted to trusted frontend origin only (`localhost:5173`)
- All secrets stored in `.env` — never hardcoded
- Firebase Realtime DB security rules deny all direct client access
- Donor emails purged after 30 days; no PII stored in vector embeddings

---

## ⚙️ Performance

| Metric | Target |
|---|---|
| Frontend initial load | < 2 seconds |
| Route transitions | < 300ms |
| Auth endpoint | < 500ms |
| Analytics queries | < 1 second |
| Quiz generation (AI-bound) | 5–10 seconds |
| ChromaDB vector search | < 50ms |
| Gemini embedding speed | < 100ms |
| Concurrent users supported | 50+ |

Reliability is ensured via exponential backoff retry (up to 3 retries with jitter) on all Gemini API calls, with a graceful fallback response if all retries fail.

---

## 🚀 How to Run Locally

### Prerequisites

Make sure you have the following installed:
- [Node.js](https://nodejs.org/) (v18 or higher)
- [Python](https://www.python.org/) (3.10 or higher)
- [Git](https://git-scm.com/)
- A [Google Gemini API Key](https://aistudio.google.com/app/apikey)
- A [Firebase Project](https://console.firebase.google.com/) with:
  - Authentication enabled (Email/Password)
  - Realtime Database created
  - Service Account JSON downloaded

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/anushkakashyap31/QuizBot.git
cd QuizBot
```

---

### Step 2 — Backend Setup

#### 2a. Navigate to the backend folder

```bash
cd backend
```

#### 2b. Create a virtual environment and activate it

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

#### 2c. Install Python dependencies

```bash
pip install -r requirements.txt
```

#### 2d. Add Firebase credentials

Place your Firebase service account JSON file in the `backend/` folder and rename it:
```
backend/firebase_credentials.json
```

#### 2e. Create the `.env` file

Create a `.env` file inside the `backend/` folder with the following content:

```env
# Google Gemini
GEMINI_API_KEY=your_gemini_api_key_here

# Firebase
FIREBASE_CREDENTIALS_PATH=firebase_credentials.json
FIREBASE_DATABASE_URL=https://your-project-id-default-rtdb.firebaseio.com

# JWT
JWT_SECRET_KEY=your_jwt_secret_key_here
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
```

#### 2f. Start the backend server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`  
Interactive API docs: `http://localhost:8000/docs`

---

### Step 3 — Frontend Setup

#### 3a. Open a new terminal and navigate to the frontend folder

```bash
cd frontend
```

#### 3b. Install Node dependencies

```bash
npm install
```

#### 3c. Create the `.env` file

Create a `.env` file inside the `frontend/` folder with your Firebase project configuration:

```env
VITE_FIREBASE_API_KEY=your_firebase_api_key
VITE_FIREBASE_AUTH_DOMAIN=your-project-id.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project-id.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your_messaging_sender_id
VITE_FIREBASE_APP_ID=your_firebase_app_id
VITE_FIREBASE_DATABASE_URL=https://your-project-id-default-rtdb.firebaseio.com

VITE_API_BASE_URL=http://localhost:8000
```

You can find these values in your Firebase project settings under **Project Settings → Your Apps → SDK setup**.

#### 3d. Start the frontend development server

```bash
npm run dev
```

The app will be available at: `http://localhost:5173`

---

### Step 4 — Using the App

1. Open `http://localhost:5173` in your browser
2. Register a new account or log in
3. Paste a donor email into the input field
4. Select the number of questions (3–10)
5. Click **Generate Quiz** and wait for AI to create your quiz
6. Answer all questions and submit
7. View your score, explanations, and AI-generated summary
8. Track your progress on the Dashboard

---

## 📊 Data Model Summary

**Firebase Realtime Database**
- `users/{uid}` — email, full name, total quizzes, total score
- `quiz_history/{quiz_id}` — email content, score, results, AI summary

**SQLite (via SQLAlchemy)**
- `USERS` — uid, email, full_name, average_score
- `QUIZZES` — quiz_id, user_id, email_content, num_questions
- `QUESTIONS` — question text, options A–D, correct answer, difficulty, explanation
- `QUIZ_RESULTS` — score, correct_answers, AI summary
- `DONOR_EMAILS` — raw email content per user

**ChromaDB Vector Store**
- Collection: `donor_emails`
- Embeddings: 384-dimensional floats (all-MiniLM-L6-v2)
- Distance metric: Cosine Similarity
- Metadata: user_id, quiz_id, created_at, word_count

---

## 🗂️ Data Retention Policy

| Data | Retention |
|---|---|
| Firebase User Profile | Indefinite |
| Firebase Quiz History | 1 year |
| SQLite Quiz Questions | 90 days |
| SQLite Donor Emails | 30 days |
| ChromaDB Embeddings | 30 days |
| JWT Tokens | 1 hour (auto-expiry) |
| User Progress (SQLite) | Indefinite |

---

**Group 03D2 | Project GAI-15 | Medicaps University × Datagami | AY 2026**

---

## 📄 License

This project was developed as an academic project. All rights reserved by the team and Medicaps University and Datagami.
