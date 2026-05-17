# ATS Lite — Project Credentials & Information
### Vimansh Technologies Backend Internship Assignment

**GitHub Repository:** https://github.com/thepranit45/vimanshtask

---

## How to Run the Project (Local)

```bash
# 1. Navigate to project folder
cd "c:\Users\thepr\OneDrive\Desktop\Vimansh Task"

# 2. Install dependencies (already done)
pip install -r requirements.txt

# 3. Apply migrations (already done)
python manage.py migrate

# 4. Seed sample data (already done)
python manage.py seed_data

# 5. Start the server
python manage.py runserver 9000
```

---

## Login Credentials

### Recruiter Account (manages jobs, views candidates, gets notifications)
| Field    | Value           |
|----------|-----------------|
| Username | `recruiter`     |
| Password | `recruiter123`  |
| Role     | Recruiter       |
| Login URL | http://127.0.0.1:9000/login/ |
| Dashboard | http://127.0.0.1:9000/ |

### Admin / Superuser Account (Django Admin Panel)
| Field    | Value           |
|----------|-----------------|
| Username | `admin`         |
| Password | `admin123`      |
| Role     | Superuser       |
| Admin URL | http://127.0.0.1:9000/admin/ |

### Candidate Account (browse jobs, apply, track applications)
> Candidates register at http://127.0.0.1:9000/candidate/register/
> The same login page http://127.0.0.1:9000/login/ works for both

| Field    | Value               |
|----------|---------------------|
| Username | `testcandidate`     |
| Password | `test1234`          |
| Role     | Candidate           |
| Login URL | http://127.0.0.1:9000/login/ |
| Dashboard | http://127.0.0.1:9000/candidate/dashboard/ |

---

## All URLs at a Glance

### Public URLs (no login required)
| URL | Description |
|-----|-------------|
| http://127.0.0.1:9000/login/ | Login (recruiter or candidate) |
| http://127.0.0.1:9000/register/ | Recruiter registration |
| http://127.0.0.1:9000/candidate/register/ | Candidate registration |
| http://127.0.0.1:9000/apply/{job_id}/ | Public job apply form |

### Recruiter Portal (login as recruiter)
| URL | Description |
|-----|-------------|
| http://127.0.0.1:9000/ | Dashboard with stats |
| http://127.0.0.1:9000/jobs/ | View / create / delete jobs |
| http://127.0.0.1:9000/jobs/{id}/ | Job detail + candidates |
| http://127.0.0.1:9000/candidates/ | All candidates sorted by score |
| http://127.0.0.1:9000/notifications/ | Notifications (read/unread) |
| http://127.0.0.1:9000/admin/ | Django admin panel |

### Candidate Portal (login as candidate)
| URL | Description |
|-----|-------------|
| http://127.0.0.1:9000/candidate/dashboard/ | Candidate home |
| http://127.0.0.1:9000/candidate/jobs/ | Browse open jobs |
| http://127.0.0.1:9000/candidate/my-applications/ | My submitted applications + scores |

---

## REST API Endpoints

> Base URL: http://127.0.0.1:9000/api/
> Authentication: Use session cookie (browser) OR JWT Bearer token (API clients)

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/register/ | Register recruiter |
| POST | /api/auth/login/ | Login → get JWT token |
| GET  | /api/auth/me/ | Current user info |
| POST | /api/auth/token/refresh/ | Refresh JWT token |

### Jobs
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET  | /api/jobs/ | List all jobs |
| POST | /api/jobs/ | Create a job |
| GET  | /api/jobs/{id}/ | Job detail |
| PUT  | /api/jobs/{id}/ | Update job |
| DELETE | /api/jobs/{id}/ | Delete job |
| GET  | /api/jobs/{id}/candidates/ | Candidates sorted by score |
| POST | /api/jobs/{id}/apply/ | Submit application |
| GET  | /api/jobs/skills/ | List skills |
| POST | /api/jobs/skills/ | Create skill |

### Candidates
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET  | /api/candidates/ | All applications (paginated) |
| GET  | /api/candidates/{id}/ | Application detail |
| PATCH | /api/candidates/{id}/ | Update status |

### Notifications
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET  | /api/notifications/ | List my notifications |
| PATCH | /api/notifications/{id}/read/ | Mark as read |
| PATCH | /api/notifications/{id}/unread/ | Mark as unread |
| PATCH | /api/notifications/mark-all-read/ | Mark all as read |

### Query Parameters (Filters)
| Endpoint | Param | Example |
|----------|-------|---------|
| /api/jobs/ | search | ?search=django |
| /api/jobs/ | status | ?status=open |
| /api/jobs/ | skill | ?skill=python |
| /api/jobs/{id}/candidates/ | score_min | ?score_min=50 |
| /api/jobs/{id}/candidates/ | search | ?search=alice |
| /api/candidates/ | score_min | ?score_min=70 |
| /api/candidates/ | job_id | ?job_id=1 |
| /api/candidates/ | status | ?status=pending |
| /api/candidates/ | search | ?search=bob |
| /api/notifications/ | is_read | ?is_read=false |

---

## Sample API Usage (curl)

### 1. Login and get token
```bash
curl -X POST http://127.0.0.1:9000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "recruiter", "password": "recruiter123"}'
```

### 2. Create a job
```bash
curl -X POST http://127.0.0.1:9000/api/jobs/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: <csrf_token>" \
  --cookie "sessionid=<session>" \
  -d '{"title": "Python Developer", "required_skill_names": ["python", "django"], "status": "open"}'
```

### 3. Apply for job (with skills)
```bash
curl -X POST http://127.0.0.1:9000/api/jobs/1/apply/ \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "skill_names": ["python", "django", "sql"]}'
```

### 4. Get candidates sorted by score
```bash
curl http://127.0.0.1:9000/api/jobs/1/candidates/?score_min=50
```

---

## Database Schema

```
User (Django built-in)
  └── UserProfile: role (recruiter | candidate | admin)

Skill: id, name

Job: id, title, description, required_skills(M2M→Skill),
     posted_by(→User), status, created_at, updated_at

Application: id, job(→Job), name, email, skills(M2M→Skill),
             resume(file), score(%), summary(AI text),
             status, applied_at

Notification: id, user(→User), message, is_read,
              created_at, application_id, job_title, candidate_name
```

## Skill Matching Formula
```
score = (candidate_skills ∩ job.required_skills) / job.required_skills × 100%

Examples:
  Job needs: python, django, sql, git, rest api  (5 skills)
  Candidate has: python, django, git              → 3/5 = 60%
  Candidate has: python, django, sql, git, rest   → 5/5 = 100%
  Candidate has: javascript, react               → 0/5 = 0%
  Job has no required skills                     → 100% (everyone qualifies)
```

---

## Project Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.13 |
| Framework | Django 5.0 |
| REST API | Django REST Framework 3.16 |
| Auth (API) | JWT via SimpleJWT |
| Auth (Web) | Django Session Auth |
| Database | SQLite (db.sqlite3) |
| Resume Parsing | PyPDF2, python-docx |
| Frontend | Django Templates + Vanilla CSS |
| Icons | Font Awesome 6.5 |
| Fonts | Google Fonts (Inter) |
| Deployment Ready | Gunicorn |

---

## Sample Data (Pre-loaded)

### Jobs
| # | Title | Required Skills |
|---|-------|----------------|
| 1 | Backend Developer (Django) | python, django, rest api, sql, git |
| 2 | Full Stack Engineer | javascript, react, nodejs, html, css, git |
| 3 | Data Engineer | python, sql, pandas, data analysis, aws |

### Candidates & Scores
| Name | Job | Skills | Score |
|------|-----|--------|-------|
| Alice Johnson | Backend Developer | python, django, rest api, sql, git, docker | **100%** |
| Bob Smith | Backend Developer | python, django, git | **60%** |
| Carol White | Backend Developer | javascript, html, css | **0%** |
| David Lee | Full Stack Engineer | javascript, react, nodejs, html, css, git | **100%** |
| Emma Davis | Full Stack Engineer | javascript, react, html | **50%** |
| Frank Chen | Data Engineer | python, sql, pandas, data analysis, aws, numpy | **100%** |

---

## Features Implemented

### Core Requirements ✅
- [x] Create Job API with title and required skills
- [x] Candidate apply with name, email, skills
- [x] SQLite database storage
- [x] Skill matching score (%) — sorted descending
- [x] Candidates returned sorted by score

### Notification System ✅
- [x] Auto-notification on every new application
- [x] API to fetch notifications with unread count
- [x] Mark individual as read / unread
- [x] Mark all as read
- [x] Timestamp + user reference stored

### Frontend ✅
- [x] Login page (recruiter + candidate, same page)
- [x] Recruiter dashboard (stats + recent activity)
- [x] Job listing page (create/delete with modal)
- [x] Job detail page (candidates + scores + filters)
- [x] Candidate listing page with scores (medal ranking)
- [x] Notification display (real-time toggle)
- [x] Candidate registration page
- [x] Candidate dashboard
- [x] Candidate browse jobs page
- [x] Candidate my applications page
- [x] Public job apply form (shareable link)

### Bonus Features ✅
- [x] Resume upload (PDF / DOCX / TXT)
- [x] Resume skill auto-extraction
- [x] AI candidate summary (skill gap analysis)
- [x] Score filtering (?score_min=X)
- [x] Pagination (page_size=10, configurable)
- [x] Search on all endpoints
- [x] Django Admin panel configured
- [x] Seed management command
- [x] Deployment-ready (Gunicorn + Render instructions)

---

## Deploy on PythonAnywhere (Free Hosting)

### Step 1 — Create account
Go to https://www.pythonanywhere.com → Sign Up (free account is enough)

### Step 2 — Open a Bash console
Dashboard → **Consoles** → **New console: Bash**

### Step 3 — Clone your GitHub repo
```bash
git clone https://github.com/thepranit45/vimanshtask.git
cd vimanshtask
```

### Step 4 — Create a virtual environment and install packages
```bash
mkvirtualenv ats_env --python=python3.10
pip install -r requirements.txt
```

### Step 5 — Set up the database
```bash
python manage.py migrate
python manage.py seed_data
```

### Step 6 — Collect static files
```bash
python manage.py collectstatic --noinput
```

### Step 7 — Configure the Web App
1. Go to PythonAnywhere **Dashboard → Web → Add a new web app**
2. Choose **Manual configuration** → **Python 3.10**
3. Set these fields:

| Field | Value |
|-------|-------|
| Source code | `/home/<your-username>/vimanshtask` |
| Virtualenv | `/home/<your-username>/.virtualenvs/ats_env` |
| WSGI file | click the link to edit it |

### Step 8 — Edit the WSGI file
Replace everything in the WSGI file with:
```python
import sys
import os

path = '/home/<your-username>/vimanshtask'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'ats_project.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```
> Replace `<your-username>` with your actual PythonAnywhere username

### Step 9 — Update settings.py for PythonAnywhere
In `ats_project/settings.py`, update these two lines:
```python
DEBUG = False
ALLOWED_HOSTS = ['<your-username>.pythonanywhere.com', '127.0.0.1']
```

### Step 10 — Reload the web app
Click **Reload** on the Web tab.
Your site will be live at: `https://<your-username>.pythonanywhere.com`

### Quick summary of all commands
```bash
git clone https://github.com/thepranit45/vimanshtask.git
cd vimanshtask
mkvirtualenv ats_env --python=python3.10
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py collectstatic --noinput
```
