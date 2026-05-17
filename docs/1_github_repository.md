# 1. GitHub Repository

## Repository Link
**https://github.com/thepranit45/vimanshtask**

---

## Repository Structure

```
vimanshtask/
├── accounts/                   # Auth app (login, register, recruiter/candidate views)
│   ├── migrations/
│   ├── frontend_urls.py        # Web UI URL routes
│   ├── frontend_views.py       # Web UI views (login, register, dashboard)
│   ├── models.py               # UserProfile model (role: recruiter/candidate)
│   ├── urls.py                 # API auth URLs
│   └── views.py                # API auth views (register, login, JWT)
│
├── ats_project/                # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── candidates/                 # Candidate/Application app
│   ├── migrations/
│   ├── models.py               # Application model + skill matching logic
│   ├── serializers.py          # DRF serializers
│   ├── urls.py
│   └── views.py                # Application API views + resume parsing
│
├── jobs/                       # Job app
│   ├── management/commands/
│   │   └── seed_data.py        # Sample data seeder
│   ├── migrations/
│   ├── models.py               # Job + Skill models
│   ├── serializers.py
│   ├── urls.py
│   └── views.py                # Job API views
│
├── notifications/              # Notification app
│   ├── migrations/
│   ├── models.py               # Notification model
│   ├── serializers.py
│   ├── urls.py
│   └── views.py                # Notification API views
│
├── templates/                  # HTML templates
│   ├── candidate/              # Candidate portal templates
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── jobs.html
│   │   ├── my_applications.html
│   │   └── register.html
│   ├── candidates/list.html    # Recruiter candidate list
│   ├── jobs/                   # Recruiter job templates
│   ├── notifications/          # Notification templates
│   ├── apply.html              # Public apply form
│   ├── base.html               # Recruiter base layout
│   ├── dashboard.html          # Recruiter dashboard
│   ├── login.html
│   └── register.html
│
├── docs/                       # This folder — project documentation
│   ├── 1_github_repository.md
│   ├── 2_readme_setup.md
│   ├── 3_api_documentation.md
│   └── 4_deployment.md
│
├── .gitignore
├── CREDENTIALS_AND_INFO.md     # All credentials & project info
├── manage.py
├── README.md
└── requirements.txt
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.13 |
| Framework | Django 5.0 |
| REST API | Django REST Framework 3.16 |
| Auth (API) | JWT — SimpleJWT |
| Auth (Web) | Django Session Auth |
| Database | SQLite |
| Resume Parsing | PyPDF2, python-docx |
| Frontend | Django Templates, Vanilla CSS |
| Deployment | Gunicorn / PythonAnywhere |

---

## Clone & Run

```bash
git clone https://github.com/thepranit45/vimanshtask.git
cd vimanshtask
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```
