# 4. Deployment

## GitHub Repository
**https://github.com/thepranit45/vimanshtask**

---

## Deployed Link (PythonAnywhere)

> After deploying on PythonAnywhere, your live URL will be:
> **`https://<your-pythonanywhere-username>.pythonanywhere.com`**

To deploy, follow the steps below.

---

## Deploy on PythonAnywhere (Free)

### Step 1 — Create Account
- Go to: https://www.pythonanywhere.com
- Sign up for a **free Beginner account**
- Your username becomes part of your URL: `https://<username>.pythonanywhere.com`

---

### Step 2 — Open Bash Console
Dashboard → **Consoles** → **Bash**

---

### Step 3 — Clone the Repo
```bash
git clone https://github.com/thepranit45/vimanshtask.git
cd vimanshtask
```

---

### Step 4 — Create Virtual Environment
```bash
mkvirtualenv ats_env --python=python3.10
```

---

### Step 5 — Install Requirements
```bash
pip install -r requirements.txt
```

---

### Step 6 — Edit settings.py
```bash
nano ats_project/settings.py
```
Change:
```python
DEBUG = False
ALLOWED_HOSTS = ['<your-username>.pythonanywhere.com', '127.0.0.1']
```
Save: `Ctrl+O` → `Enter` → `Ctrl+X`

---

### Step 7 — Set Up Database & Static Files
```bash
python manage.py migrate
python manage.py seed_data
python manage.py collectstatic --noinput
```

---

### Step 8 — Create the Web App
1. Go to **Dashboard → Web → Add a new web app**
2. Select **Manual configuration** → **Python 3.10**

---

### Step 9 — Configure Web App Settings (Web tab)

| Setting | Value |
|---------|-------|
| Source code | `/home/<username>/vimanshtask` |
| Virtualenv | `/home/<username>/.virtualenvs/ats_env` |

**Static files section:**

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/<username>/vimanshtask/staticfiles` |
| `/media/` | `/home/<username>/vimanshtask/media` |

---

### Step 10 — Edit WSGI File
Click the WSGI file link on the Web tab → delete all contents → paste:

```python
import sys, os

path = '/home/<your-username>/vimanshtask'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'ats_project.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Click **Save**.

---

### Step 11 — Reload
Click the green **Reload** button on the Web tab.

Your site is now live at:
**`https://<your-username>.pythonanywhere.com`**

---

## Alternative: Deploy on Render (also free)

### Step 1 — Create account at https://render.com

### Step 2 — New Web Service → Connect GitHub repo

### Step 3 — Configure:

| Setting | Value |
|---------|-------|
| Build Command | `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput` |
| Start Command | `gunicorn ats_project.wsgi:application` |
| Environment | Python 3 |

### Step 4 — Add Environment Variables:
| Key | Value |
|-----|-------|
| `DEBUG` | `False` |
| `SECRET_KEY` | *(generate a new secret key)* |
| `ALLOWED_HOSTS` | `your-app.onrender.com` |

### Step 5 — Deploy
Click **Deploy** → wait ~2 minutes → live!

---

## Notes for Production

- `DEBUG = False` in settings.py
- `SECRET_KEY` should be stored as an environment variable, not in code
- Use PostgreSQL instead of SQLite for production (Render provides free PostgreSQL)
- Run `collectstatic` before deployment for static files to work
