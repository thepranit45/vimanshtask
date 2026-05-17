# ATS Lite - Applicant Tracking System
### Vimansh Technologies Backend Internship Assignment

A full-featured **Applicant Tracking System (ATS)** built with Django, Django REST Framework, and a modern dark-mode UI. Features job posting, candidate applications, skill-based matching scoring, notifications, resume parsing, and AI-generated candidate summaries.

---

## Features Implemented

### Core Tasks
- [x] **Job API** - Create jobs with title, description, and required skills
- [x] **Candidate Applications** - Apply with name, email, skills (+ resume upload)
- [x] **Database** - SQLite with proper relational schema
- [x] **Skill Matching Score** - Auto-calculated `(matched skills / required skills) * 100%`
- [x] **Candidates sorted by score** - Descending order on all candidate views

### Notification System
- [x] Auto-create notifications when candidate applies
- [x] API to fetch notifications with unread count
- [x] Mark individual notification as read/unread
- [x] Mark all notifications as read
- [x] Timestamp and user reference stored

### Frontend UI
- [x] **Login page** - Beautiful dark-mode with animated background
- [x] **Register page** - Recruiter signup
- [x] **Dashboard** - Stats overview (jobs, applications, avg score, unread notifs)
- [x] **Job listing page** - Create/delete/view jobs with required skills
- [x] **Candidate listing page** - Ranked by score with medal icons (Gold/Silver/Bronze)
- [x] **Job detail page** - Candidates for specific job with score bars
- [x] **Notification display** - Real-time read/unread toggle
- [x] **Public Apply page** - Shareable link for candidates to apply

### Bonus Features
- [x] **Resume upload** - PDF/DOCX/TXT support
- [x] **Resume skill auto-extraction** - Skills auto-extracted from uploaded resume
- [x] **AI-based candidate summary** - Auto-generated text based on skill match analysis
- [x] **Score filtering** - `?score_min=X` parameter on all candidate endpoints
- [x] **Pagination** - Built-in DRF pagination (10 per page)
- [x] **Search** - Search candidates by name/email/job title
- [x] **Admin Panel** - Full Django admin for all models

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 5.0, Python 3.13 |
| API | Django REST Framework 3.16 |
| Auth | JWT (SimpleJWT) + Django Sessions |
| Database | SQLite (easily swappable to PostgreSQL) |
| Resume Parsing | PyPDF2, python-docx |
| Frontend | Django Templates, Vanilla CSS, Font Awesome |
| Deployment | Gunicorn ready |

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd ats-lite
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Apply database migrations
```bash
python manage.py migrate
```

### 4. Seed sample data (optional but recommended)
```bash
python manage.py seed_data
```

### 5. Create a superuser (for admin panel)
```bash
python manage.py createsuperuser
```

### 6. Run the development server
```bash
python manage.py runserver
```

### 7. Access the application
| URL | Description |
|-----|-------------|
| http://127.0.0.1:8000/ | Dashboard (login required) |
| http://127.0.0.1:8000/login/ | Login page |
| http://127.0.0.1:8000/register/ | Register as recruiter |
| http://127.0.0.1:8000/jobs/ | Job listings |
| http://127.0.0.1:8000/candidates/ | Candidate listings with scores |
| http://127.0.0.1:8000/notifications/ | Notifications |
| http://127.0.0.1:8000/admin/ | Django admin panel |
| http://127.0.0.1:8000/apply/{job_id}/ | Public candidate apply form |

### Demo credentials (after `seed_data`):
```
Username: recruiter
Password: recruiter123

Admin: admin / admin123
```

---

## API Documentation

### Authentication
All API endpoints require JWT token in header: `Authorization: Bearer <access_token>`

#### Register
```
POST /api/auth/register/
Body: { "username": "...", "email": "...", "password": "..." }
```

#### Login
```
POST /api/auth/login/
Body: { "username": "...", "password": "..." }
Response: { "access": "<token>", "refresh": "<token>", "username": "..." }
```

---

### Jobs API

#### List all jobs (public)
```
GET /api/jobs/
Query params: ?search=title, ?status=open, ?skill=python, ?ordering=-created_at
```

#### Create a job (authenticated)
```
POST /api/jobs/
Body: {
  "title": "Backend Developer",
  "description": "...",
  "required_skill_names": ["python", "django", "sql"],
  "status": "open"
}
```

#### Get job detail
```
GET /api/jobs/{id}/
```

#### Get candidates for a job (sorted by score)
```
GET /api/jobs/{id}/candidates/
Query params: ?score_min=50, ?search=alice
```

#### Apply for a job
```
POST /api/jobs/{job_id}/apply/
Body (multipart/form-data):
  name: "Alice Johnson"
  email: "alice@example.com"
  skill_names: "python,django,sql"
  resume: <file>  (optional)
```

---

### Candidates API

#### List all applications (authenticated, paginated)
```
GET /api/candidates/
Query params: ?job_id=1, ?score_min=60, ?search=alice, ?status=pending, ?ordering=-score
```

#### Get application detail
```
GET /api/candidates/{id}/
```

---

### Skills API

#### List/create skills
```
GET  /api/jobs/skills/
POST /api/jobs/skills/
Body: { "name": "python" }
```

---

### Notifications API

#### List notifications (authenticated)
```
GET /api/notifications/
Query params: ?is_read=false
Response: { "total": 5, "unread_count": 3, "notifications": [...] }
```

#### Mark notification as read/unread
```
PATCH /api/notifications/{id}/read/
PATCH /api/notifications/{id}/unread/
```

#### Mark all as read
```
PATCH /api/notifications/mark-all-read/
```

---

## Database Schema

```
Skill          : id, name
Job            : id, title, description, required_skills(M2M), posted_by, status, created_at
Application    : id, job, name, email, skills(M2M), resume, score, summary, status, applied_at
Notification   : id, user, message, is_read, created_at, application_id, job_title, candidate_name
UserProfile    : id, user, role, created_at
```

## Skill Matching Logic

```python
score = (len(matched_skills) / len(required_skills)) * 100
# matched_skills = candidate.skills ∩ job.required_skills
# Returns 100.0 if job has no required skills
```

## Business Logic - Edge Cases Handled
- Duplicate application prevention (same email + job)
- Job status check (only `open` jobs accept applications)
- Empty required skills (score = 100%)
- Resume skill auto-extraction merges with manually entered skills
- Score recalculated on application save
- Notifications auto-created for job poster only

---

## Deployment (Render)

1. Add `gunicorn` to `requirements.txt` (already included)
2. Set `DEBUG=False` and configure `ALLOWED_HOSTS`
3. Set `DATABASE_URL` environment variable for PostgreSQL
4. Render build command: `pip install -r requirements.txt && python manage.py migrate`
5. Render start command: `gunicorn ats_project.wsgi:application`
