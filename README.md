# GradeTrack — GPA & CGPA Calculator

A complete Django web application for Annamalai University students to calculate GPA, track CGPA, and monitor academic performance semester by semester.

**Grading Scale:** S=10 | A=9 | B=8 | C=7 | D=6 | E=5 | RA=0
**Percentage Formula:** (CGPA − 0.25) × 10

---

## Features

- GPA Calculator (credit-weighted, live grade auto-fill)
- CGPA / OGPA Calculator with percentage conversion
- Target CGPA Calculator (Honours ≥ 8.25, First Class ≥ 6.75)
- Student Dashboard with GPA/CGPA charts
- Semester & Subject management
- Custom Grading System configuration
- User accounts (register / login / logout)
- Django Admin panel
- Degree classification (Honours / First Class with Distinction / First Class / Second Class)

---

## Technology Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, Django 4.2+ |
| Frontend | Bootstrap 5, Chart.js, JavaScript |
| Database | SQLite (dev) / PostgreSQL (production) |
| Static files | WhiteNoise |
| Deployment | Railway (free) |

---

## Local Development

### 1. Clone & enter project
```bash
git clone https://github.com/YOUR_USERNAME/gpa-cgpa-calculator.git
cd gpa-cgpa-calculator
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create .env file
```bash
copy .env.example .env      # Windows
cp .env.example .env        # Mac/Linux
```

Edit `.env`:
```
SECRET_KEY=any-random-long-string-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Create superuser (admin)
```bash
python manage.py createsuperuser
```

### 7. Start server
```bash
python manage.py runserver
```

Open → http://127.0.0.1:8000

---

## Deploy to Railway (Free Hosting)

Railway gives you **free hosting** with a PostgreSQL database included.

### Step 1 — Push code to GitHub

1. Create a free account at https://github.com
2. Create a new repository called `gpa-cgpa-calculator`
3. Open terminal in your project folder and run:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/gpa-cgpa-calculator.git
git push -u origin main
```

### Step 2 — Create Railway account

1. Go to → **https://railway.app**
2. Click **"Start a New Project"**
3. Sign up with your GitHub account (free)

### Step 3 — Deploy from GitHub

1. Click **"Deploy from GitHub repo"**
2. Select your `gpa-cgpa-calculator` repository
3. Railway will auto-detect it's a Python/Django project

### Step 4 — Add PostgreSQL database

1. In your Railway project, click **"+ New"**
2. Select **"Database"** → **"PostgreSQL"**
3. Railway automatically sets `DATABASE_URL` environment variable

### Step 5 — Set environment variables

In Railway dashboard → your service → **Variables** tab, add:

| Variable | Value |
|---|---|
| `SECRET_KEY` | any long random string (e.g. `gradetrack-secret-2024-xk9p2mq`) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `your-app-name.railway.app` |

### Step 6 — Set build command

In Railway → Settings → add:

**Build Command:**
```
pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate
```

**Start Command:**
```
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2
```

### Step 7 — Deploy

Click **Deploy**. Railway will build and deploy in about 2–3 minutes.

Your live URL will be: `https://your-app-name.railway.app`

### Step 8 — Create admin user on Railway

In Railway → your service → **Shell** tab, run:
```bash
python manage.py createsuperuser
```

---

## Grading Scale (Annamalai University)

| Marks | Grade | Grade Point |
|---|---|---|
| 90–100 | S | 10 |
| 80–89 | A | 9 |
| 70–79 | B | 8 |
| 60–69 | C | 7 |
| 55–59 | D | 6 |
| 50–54 | E | 5 |
| Below 50 | RA | 0 (Excluded from GPA) |

**Percentage = (CGPA − 0.25) × 10**

---

## Degree Classification

| Class | CGPA | Credits | Condition |
|---|---|---|---|
| Honours | ≥ 8.25 | 192+ | All first attempt, 4 years |
| First Class with Distinction | ≥ 8.25 | 172+ | All first attempt, 4 years |
| First Class | ≥ 6.75 | 172+ | Within 5 years |
| Second Class | Any | 172+ | Within 7 years |

---

## Project Structure

```
gpa-cgpa-calculator/
├── config/           → Django settings, URLs
├── accounts/         → Register, login, logout
├── calculator/       → Core app (GPA, CGPA, Dashboard)
│   ├── calculations.py  → Pure calculation logic
│   ├── models.py        → Database models
│   ├── views.py         → All views
│   └── tests.py         → Unit tests
├── templates/        → HTML templates
├── static/           → CSS, JavaScript
├── Procfile          → For Railway/Render deployment
├── build.sh          → Build script
├── runtime.txt       → Python version
└── requirements.txt  → Dependencies
```

---

## Run Tests

```bash
python manage.py test calculator
```

---

## Author

Built for Annamalai University Faculty of Engineering & Technology students.
