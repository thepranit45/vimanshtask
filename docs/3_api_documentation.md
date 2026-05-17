# 3. API Documentation

## Base URL
```
http://127.0.0.1:8000/api/
```

## Authentication

The API supports two authentication methods:

| Method | Use Case | How |
|--------|----------|-----|
| **JWT Bearer Token** | REST API clients (Postman, curl) | `Authorization: Bearer <access_token>` |
| **Session Cookie** | Browser-based web UI | Automatic after login |

---

## Auth Endpoints

### Register (Recruiter)
```
POST /api/auth/register/
```
**Request Body:**
```json
{
  "username": "myrecruiter",
  "email": "recruiter@company.com",
  "password": "mypassword123"
}
```
**Response:**
```json
{
  "message": "User registered successfully",
  "username": "myrecruiter"
}
```

---

### Login → Get JWT Token
```
POST /api/auth/login/
```
**Request Body:**
```json
{
  "username": "recruiter",
  "password": "recruiter123"
}
```
**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "username": "recruiter",
  "role": "recruiter"
}
```
> Use the `access` token in all subsequent requests

---

### Refresh Token
```
POST /api/auth/token/refresh/
```
```json
{ "refresh": "<refresh_token>" }
```

---

### Current User
```
GET /api/auth/me/
```
Returns logged-in user's info.

---

## Jobs API

### List All Jobs
```
GET /api/jobs/
```
**Query Parameters:**

| Param | Type | Example | Description |
|-------|------|---------|-------------|
| `search` | string | `?search=django` | Filter by title |
| `status` | string | `?status=open` | Filter by status (open/closed) |
| `skill` | string | `?skill=python` | Filter by required skill |
| `ordering` | string | `?ordering=-created_at` | Sort results |

**Response:**
```json
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "title": "Backend Developer (Django)",
      "description": "Build REST APIs...",
      "required_skills": [
        {"id": 1, "name": "python"},
        {"id": 2, "name": "django"}
      ],
      "status": "open",
      "posted_by": "recruiter",
      "application_count": 3,
      "created_at": "2026-05-17T03:15:00Z"
    }
  ]
}
```

---

### Create a Job *(auth required)*
```
POST /api/jobs/
```
**Request Body:**
```json
{
  "title": "Python Developer",
  "description": "Build and maintain backend APIs",
  "required_skill_names": ["python", "django", "sql"],
  "status": "open"
}
```
**Response:** `201 Created` with job object.

---

### Get Job Detail
```
GET /api/jobs/{id}/
```

---

### Update Job *(auth required)*
```
PUT /api/jobs/{id}/
PATCH /api/jobs/{id}/
```

---

### Delete Job *(auth required)*
```
DELETE /api/jobs/{id}/
```
Response: `204 No Content`

---

### Get Candidates for a Job (sorted by score)
```
GET /api/jobs/{id}/candidates/
```
**Query Parameters:**

| Param | Example | Description |
|-------|---------|-------------|
| `score_min` | `?score_min=50` | Only show candidates with score ≥ 50% |
| `search` | `?search=alice` | Filter by candidate name/email |

**Response:**
```json
[
  {
    "id": 1,
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "skills": [{"id": 1, "name": "python"}, {"id": 2, "name": "django"}],
    "score": 100.0,
    "summary": "Excellent match. Candidate has all 5 required skills...",
    "status": "pending",
    "applied_at": "2026-05-17T03:15:00Z"
  }
]
```

---

### Apply for a Job *(public — no auth needed)*
```
POST /api/jobs/{job_id}/apply/
```
**Request Body (multipart/form-data for resume, or JSON):**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "skill_names": "python,django,sql,git"
}
```
Or with resume file (multipart):
```
name=John Doe
email=john@example.com
skill_names=python,django,sql
resume=<file upload>
```
**Response:**
```json
{
  "id": 7,
  "name": "John Doe",
  "email": "john@example.com",
  "score": 80.0,
  "summary": "Strong match. Candidate has 4 of 5 required skills...",
  "status": "pending"
}
```

---

## Skills API

### List All Skills
```
GET /api/jobs/skills/
```
**Response:**
```json
[
  {"id": 1, "name": "python"},
  {"id": 2, "name": "django"},
  {"id": 3, "name": "sql"}
]
```

### Create a Skill *(auth required)*
```
POST /api/jobs/skills/
```
```json
{ "name": "fastapi" }
```

---

## Candidates API

### List All Applications *(auth required)*
```
GET /api/candidates/
```
**Query Parameters:**

| Param | Example | Description |
|-------|---------|-------------|
| `job_id` | `?job_id=1` | Filter by job |
| `score_min` | `?score_min=70` | Min match score |
| `status` | `?status=pending` | Filter by status |
| `search` | `?search=alice` | Search by name/email |
| `ordering` | `?ordering=-score` | Sort results |
| `page` | `?page=2` | Pagination (10 per page) |

**Response (paginated):**
```json
{
  "count": 6,
  "next": null,
  "previous": null,
  "results": [...]
}
```

### Get Application Detail *(auth required)*
```
GET /api/candidates/{id}/
```

### Update Application Status *(auth required)*
```
PATCH /api/candidates/{id}/
```
```json
{ "status": "shortlisted" }
```
Valid statuses: `pending`, `shortlisted`, `rejected`, `hired`

---

## Notifications API

### List My Notifications *(auth required)*
```
GET /api/notifications/
```
**Query Parameters:**

| Param | Example | Description |
|-------|---------|-------------|
| `is_read` | `?is_read=false` | Filter unread only |

**Response:**
```json
{
  "total": 6,
  "unread_count": 3,
  "notifications": [
    {
      "id": 1,
      "message": "New application from Alice Johnson for 'Backend Developer' - Score: 100.0%",
      "is_read": false,
      "candidate_name": "Alice Johnson",
      "job_title": "Backend Developer (Django)",
      "created_at": "2026-05-17T03:15:00Z"
    }
  ]
}
```

### Mark as Read
```
PATCH /api/notifications/{id}/read/
```

### Mark as Unread
```
PATCH /api/notifications/{id}/unread/
```

### Mark All as Read
```
PATCH /api/notifications/mark-all-read/
```

---

## Skill Matching Logic

```
score = (candidate_skills ∩ job.required_skills) / len(job.required_skills) × 100

Special cases:
  • Job has no required skills → score = 100%
  • Candidate has no skills    → score = 0%
```

**Examples:**

| Job Required Skills | Candidate Skills | Score |
|--------------------|-----------------|-------|
| python, django, sql, git, rest (5) | python, django, git | 3/5 = **60%** |
| python, django, sql, git, rest (5) | python, django, sql, git, rest | 5/5 = **100%** |
| python, django, sql, git, rest (5) | javascript, react | 0/5 = **0%** |
| (none required) | anything | **100%** |

---

## Sample curl Commands

### Login
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"recruiter","password":"recruiter123"}'
```

### Create Job (with JWT)
```bash
curl -X POST http://127.0.0.1:8000/api/jobs/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{"title":"Python Dev","required_skill_names":["python","django"],"status":"open"}'
```

### Apply for Job (public)
```bash
curl -X POST http://127.0.0.1:8000/api/jobs/1/apply/ \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@test.com","skill_names":"python,django,sql"}'
```

### Get Candidates Sorted by Score
```bash
curl http://127.0.0.1:8000/api/jobs/1/candidates/ \
  -H "Authorization: Bearer <access_token>"
```

### Filter candidates with score > 50
```bash
curl "http://127.0.0.1:8000/api/jobs/1/candidates/?score_min=50" \
  -H "Authorization: Bearer <access_token>"
```

### Get Unread Notifications
```bash
curl "http://127.0.0.1:8000/api/notifications/?is_read=false" \
  -H "Authorization: Bearer <access_token>"
```
