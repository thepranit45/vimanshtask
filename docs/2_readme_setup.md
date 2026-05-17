# 2. README — Setup Instructions

## ATS Lite — Applicant Tracking System
**Vimansh Technologies Backend Internship Assignment**

A full-featured Applicant Tracking System built with Django, REST Framework, JWT authentication, skill-based candidate matching, and a modern dark-mode UI.

---

## Prerequisites

| Requirement | Version |
|------------|---------|
| Python | 3.10 or higher |
| pip | latest |
| Git | any |

---

## Local Setup — Step by Step

### Step 1: Clone the repository
```bash
git clone https://github.com/thepranit45/vimanshtask.git
cd vimanshtask
```

### Step 2: Create and activate a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

**Packages installed:**
- `django` — web framework
- `djangorestframework` — REST API
- `djangorestframework-simplejwt` — JWT authentication
- `django-cors-headers` — CORS support
- `PyPDF2` — PDF resume parsing
- `python-docx` — DOCX resume parsing
- `Pillow` — image handling
- `gunicorn` — production server

### Step 4: Apply database migrations
```bash
python manage.py migrate
```

### Step 5: Seed sample data (optional but recommended)
```bash
python manage.py seed_data
```

This creates:
- 1 recruiter account (`recruiter` / `recruiter123`)
- 3 sample jobs with required skills
- 6 sample candidates with scores calculated
- 6 notifications

### Step 6: Create a superuser (for Django admin)
```bash
python manage.py createsuperuser
```
Or use the pre-created one: `admin` / `admin123`

### Step 7: Start the development server
```bash
python manage.py runserver
# or on a different port:
python manage.py runserver 9000
```

### Step 8: Access the app
Open your browser at: **http://127.0.0.1:8000/**

---

## Login Credentials (after seed_data)

| Role | Username | Password | Dashboard URL |
|------|----------|----------|---------------|
| Recruiter | `recruiter` | `recruiter123` | http://127.0.0.1:8000/ |
| Admin | `admin` | `admin123` | http://127.0.0.1:8000/admin/ |
| Candidate | register at `/candidate/register/` | — | http://127.0.0.1:8000/candidate/dashboard/ |

---

## Key URLs

| URL | Description |
|-----|-------------|
| `/login/` | Login (works for all roles) |
| `/register/` | Recruiter registration |
| `/candidate/register/` | Candidate registration |
| `/` | Recruiter dashboard |
| `/jobs/` | Manage jobs |
| `/candidates/` | View all candidates with scores |
| `/notifications/` | View notifications |
| `/admin/` | Django admin panel |
| `/candidate/dashboard/` | Candidate home |
| `/candidate/jobs/` | Candidate browse jobs |
| `/candidate/my-applications/` | Candidate's submitted applications |
| `/apply/<job_id>/` | Public job apply form (no login needed) |
| `/api/` | REST API root |

---

## Features

### Core
- Job creation with required skills (tagged)
- Candidate application with name, email, skills, optional resume
- Skill matching score: `matched_skills / required_skills × 100%`
- Candidates sorted by score (descending)

### Notifications
- Auto-created when a candidate applies
- Read / unread toggle (per notification or bulk)
- Unread count badge on UI

### Candidate Portal
- Separate registration and login flow
- Browse open jobs with search and skill filter
- Apply directly from the portal
- View all submitted applications with scores and AI summary

### Bonus
- Resume upload (PDF, DOCX, TXT)
- Skill auto-extraction from resume text
- AI-generated candidate summary (skill gap analysis)
- Score filter (`?score_min=70`)
- Search and pagination on all list endpoints
- Full Django admin panel

---

## Project Architecture

```
Request → Django URL Router
           ├── /api/...     → DRF Views (JSON, JWT auth)
           └── /...         → Template Views (HTML, session auth)

Models:
  User → UserProfile (role)
  Job ←→ Skill (M2M)
  Application → Job, Skill (M2M), User
  Notification → User, Application
```
