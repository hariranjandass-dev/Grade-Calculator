# GradeTrack — GPA & CGPA Calculator

<div align="center">

![GradeTrack Banner](https://img.shields.io/badge/GradeTrack-GPA%20%26%20CGPA%20Calculator-0d6efd?style=for-the-badge&logo=graduation-cap)

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2+-092E20?style=flat-square&logo=django&logoColor=white)](https://djangoproject.com)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=flat-square&logo=bootstrap&logoColor=white)](https://getbootstrap.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Ready-4169E1?style=flat-square&logo=postgresql&logoColor=white)](https://postgresql.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Railway](https://img.shields.io/badge/Deploy-Railway-0B0D0E?style=flat-square&logo=railway)](https://railway.app)

**A production-grade academic performance tracking system built for university students.**  
Calculate GPA, track CGPA semester by semester, predict degree classifications, and visualise academic progress — all in one place.

[Live Demo](#) · [Report Bug](#) · [Request Feature](#)

</div>

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Grading System](#grading-system)
- [GPA & CGPA Formulae](#gpa--cgpa-formulae)
- [Degree Classification](#degree-classification)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Development](#local-development)
  - [Environment Variables](#environment-variables)
- [Database](#database)
- [Running Tests](#running-tests)
- [Deployment — Railway](#deployment--railway)
- [Security](#security)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

GradeTrack is a full-stack Django web application designed for **Annamalai University — Faculty of Engineering & Technology** students. It implements the official university grading rules, percentage conversion formula, and degree classification criteria, giving students an accurate and reliable tool to track their academic journey from Semester I through Semester VIII.

The application is institution-aware yet architecturally generic — the grading scale is fully configurable, making it adaptable for any university that uses a credit-based grading system.

---

## Features

### Core Calculators
| Feature | Description |
|---|---|
| **GPA Calculator** | Credit-weighted semester GPA with live grade auto-fill as you type marks |
| **CGPA / OGPA Calculator** | Cumulative GPA across all semesters using proper credit-weighted averaging |
| **Target CGPA Calculator** | Computes the required GPA in upcoming semesters to reach a target CGPA |

### Academic Management
| Feature | Description |
|---|---|
| **Student Dashboard** | Central view of CGPA, percentage, total credits, and degree classification |
| **Semester Management** | Add, edit, and delete semesters (Semester I–VIII) |
| **Subject Management** | Manage subjects per semester with course code, credits, marks, grade, and grade points |
| **Performance Charts** | Interactive Chart.js bar chart (GPA per semester) and line chart (cumulative CGPA) |

### Configuration & Accounts
| Feature | Description |
|---|---|
| **Custom Grading System** | Configure any grading scale — the default is the official AU 10-point scale |
| **User Authentication** | Register, login, logout using Django's built-in auth system |
| **Data Isolation** | Each student sees only their own data — enforced at the queryset level |
| **Django Admin** | Full admin panel for superusers to manage all records |

---

## Technology Stack

### Backend
| Technology | Version | Purpose |
|---|---|---|
| Python | 3.11 | Core language |
| Django | 4.2+ | Web framework |
| PostgreSQL | 15 | Production database |
| SQLite | 3 | Local development database |
| Gunicorn | 21+ | WSGI HTTP server |
| WhiteNoise | 6+ | Static file serving |
| dj-database-url | 2+ | Database URL parsing |

### Frontend
| Technology | Version | Purpose |
|---|---|---|
| Bootstrap | 5.3 | UI framework |
| Chart.js | 4.4 | GPA/CGPA charts |
| Bootstrap Icons | 1.11 | Icon library |
| Vanilla JavaScript | ES5+ | Dynamic subject rows, live grade lookup |

### DevOps & Hosting
| Technology | Purpose |
|---|---|
| Railway | Free cloud hosting + managed PostgreSQL |
| GitHub | Version control + CI/CD trigger |
| python-dotenv | Environment variable management |

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                        Browser                           │
│         Bootstrap 5 + Chart.js + Vanilla JS              │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP
┌──────────────────────▼──────────────────────────────────┐
│                   Django (WSGI)                          │
│                                                          │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │  accounts/  │  │ calculator/  │  │    config/     │  │
│  │  Register   │  │  views.py    │  │  settings.py   │  │
│  │  Login      │  │  forms.py    │  │  urls.py       │  │
│  │  Logout     │  │  models.py   │  │  wsgi.py       │  │
│  └─────────────┘  │  calculations│  └────────────────┘  │
│                   │  .py         │                       │
│                   └──────┬───────┘                       │
│                          │ ORM                           │
│  ┌───────────────────────▼──────────────────────────┐   │
│  │              Django ORM Layer                     │   │
│  └───────────────────────┬──────────────────────────┘   │
└──────────────────────────┼──────────────────────────────┘
                           │
          ┌────────────────▼────────────────┐
          │         PostgreSQL               │
          │  (SQLite for local dev)          │
          │                                  │
          │  Users → StudentProfile          │
          │       → GradingSystem            │
          │           → GradeScale           │
          │       → Semester                 │
          │           → Subject              │
          └──────────────────────────────────┘
```

### Key Design Principle

Calculation logic is completely separated from views:

```
models.py → forms.py → calculations.py → views.py → templates
```

`calculations.py` contains pure functions with no Django imports — independently testable, reusable, and decoupled from HTTP concerns.

---

## Grading System

Default grading scale (Annamalai University — Faculty of Engineering & Technology):

| Marks Range | Letter Grade | Grade Point | Description |
|:-----------:|:------------:|:-----------:|-------------|
| 90 – 100 | **S** | 10 | Outstanding |
| 80 – 89 | **A** | 9 | Excellent |
| 70 – 79 | **B** | 8 | Very Good |
| 60 – 69 | **C** | 7 | Good |
| 55 – 59 | **D** | 6 | Above Average |
| 50 – 54 | **E** | 5 | Average |
| Below 50 | **RA** | 0 | Reappear (excluded from GPA) |

> **Note:** Grades **RA** (Reappear) and **W** (Withdrawn) are excluded from GPA and CGPA calculations as per university regulations.

Users can customise this scale at `/grading-system/` to suit any institution.

---

## GPA & CGPA Formulae

### Semester GPA

```
        Σ (Credit Hours × Grade Point)
GPA  =  ──────────────────────────────
              Σ (Credit Hours)

Note: RA / W grade courses are excluded from this calculation.
```

**Example — Semester I:**

| Course | Credit Hours | Grade | Grade Point | Credit × Point |
|--------|:------------:|:-----:|:-----------:|:--------------:|
| Mathematics – I | 4 | B | 8 | 32 |
| Physics | 4 | A | 9 | 36 |
| Chemistry | 4 | B | 8 | 32 |
| Programming | 3 | B | 8 | 24 |
| Heritage of Tamils | 1 | B | 8 | 8 |
| Communication Lab | 1.5 | B | 8 | 12 |
| Workshop Practices | 1.5 | A | 9 | 13.5 |
| Electrical Lab | 1.5 | A | 9 | 13.5 |
| **Total** | **20.5** | | | **171** |

```
GPA = 171 / 20.5 = 8.34
```

### Cumulative GPA (CGPA / OGPA)

```
         Σ (Semester GPA × Semester Credits)
CGPA  =  ─────────────────────────────────────
                  Σ (Total Credits)
```

> Simple average of GPAs is **not** used — each semester is weighted by its credit load.

### Percentage Conversion

```
Percentage  =  (CGPA − 0.25) × 10
```

### Target CGPA (Required Future GPA)

```
                  (Target CGPA × Total Credits) − (Current CGPA × Completed Credits)
Required GPA  =  ────────────────────────────────────────────────────────────────────
                                        Future Credits
```

---

## Degree Classification

| Classification | CGPA | Credits | Condition |
|---|:---:|:---:|---|
| **Honours** | ≥ 8.25 | 192+ | All courses cleared in first attempt; completed within 4 years |
| **First Class with Distinction** | ≥ 8.25 | 172+ | All courses cleared in first attempt; completed within 4 years |
| **First Class** | ≥ 6.75 | 172+ | Completed within 5 years |
| **Second Class** | Any | 172+ | Completed within 7 years |

---

## Project Structure

```
gpa-cgpa-calculator/
│
├── config/                         # Django project configuration
│   ├── __init__.py
│   ├── settings.py                 # Settings (dev + production)
│   ├── urls.py                     # Root URL configuration
│   ├── wsgi.py                     # WSGI entry point
│   └── asgi.py                     # ASGI entry point
│
├── accounts/                       # Authentication app
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py                    # Registration form
│   ├── models.py                   # StudentProfile model
│   ├── urls.py
│   └── views.py                    # Register, login, logout
│
├── calculator/                     # Core application
│   ├── migrations/
│   ├── admin.py                    # Django admin configuration
│   ├── apps.py
│   ├── calculations.py             # Pure calculation engine (no Django deps)
│   ├── forms.py                    # Semester, Subject, GradingSystem forms
│   ├── models.py                   # GradingSystem, GradeScale, Semester, Subject
│   ├── tests.py                    # Unit tests (25+ test cases)
│   ├── urls.py                     # App URL patterns
│   ├── validators.py               # Reusable field validators
│   └── views.py                    # All views
│
├── templates/                      # HTML templates
│   ├── base.html                   # Base layout (navbar, footer, messages)
│   ├── home.html                   # Landing page
│   ├── accounts/
│   │   ├── login.html
│   │   └── register.html
│   ├── calculator/
│   │   ├── gpa.html                # GPA Calculator
│   │   ├── cgpa.html               # CGPA Calculator
│   │   ├── target_cgpa.html        # Target CGPA Calculator
│   │   ├── grading_system.html     # Grading System configuration
│   │   ├── semester_detail.html    # Semester view with subjects table
│   │   ├── semester_form.html      # Add / Edit semester
│   │   ├── subject_form.html       # Manage subjects in a semester
│   │   └── confirm_delete.html     # Delete confirmation
│   └── dashboard/
│       └── dashboard.html          # Student dashboard with charts
│
├── static/
│   ├── css/
│   │   ├── style.css               # Global styles
│   │   ├── calculator.css          # Calculator-specific styles
│   │   └── dashboard.css           # Dashboard styles
│   └── js/
│       ├── calculator.js           # Shared utilities (auto-dismiss alerts)
│       ├── gpa.js                  # Live grade lookup, dynamic subject rows
│       ├── cgpa.js                 # Dynamic semester rows
│       └── dashboard.js            # Chart placeholders
│
├── manage.py
├── requirements.txt
├── Procfile                        # Railway / Heroku start command
├── runtime.txt                     # Python version for deployment
├── build.sh                        # Build script (migrate + collectstatic)
├── .env.example                    # Environment variable template
├── .gitignore
└── README.md
```

---

## Getting Started

### Prerequisites

| Requirement | Minimum Version | Check |
|---|---|---|
| Python | 3.10+ | `python --version` |
| pip | 23+ | `pip --version` |
| Git | 2.x | `git --version` |

### Local Development

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/gpa-cgpa-calculator.git
cd gpa-cgpa-calculator
```

**2. Create and activate virtual environment**
```bash
# Create
python -m venv venv

# Activate — Windows
venv\Scripts\activate

# Activate — Mac / Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment**
```bash
# Windows
copy .env.example .env

# Mac / Linux
cp .env.example .env
```

Edit `.env` — see [Environment Variables](#environment-variables) below.

**5. Apply migrations**
```bash
python manage.py migrate
```

**6. Create superuser**
```bash
python manage.py createsuperuser
```

**7. Start development server**
```bash
python manage.py runserver
```

| URL | Page |
|---|---|
| http://127.0.0.1:8000/ | Home |
| http://127.0.0.1:8000/gpa/ | GPA Calculator |
| http://127.0.0.1:8000/cgpa/ | CGPA Calculator |
| http://127.0.0.1:8000/target-cgpa/ | Target CGPA |
| http://127.0.0.1:8000/dashboard/ | Student Dashboard |
| http://127.0.0.1:8000/grading-system/ | Grading System |
| http://127.0.0.1:8000/admin/ | Django Admin |

---

### Environment Variables

| Variable | Required | Default | Description |
|---|:---:|---|---|
| `SECRET_KEY` | ✅ | — | Django secret key — long random string |
| `DEBUG` | ✅ | `False` | `True` for development, `False` for production |
| `ALLOWED_HOSTS` | ✅ | `localhost,127.0.0.1` | Comma-separated list of allowed hosts |
| `DATABASE_URL` | ⬜ | SQLite | PostgreSQL connection string (auto-set by Railway) |

**Generate a secure SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Database

### Models

```
User (Django built-in)
 └── StudentProfile          (one-to-one)
       ├── GradingSystem      (one-to-many)
       │     └── GradeScale   (one-to-many)
       └── Semester           (one-to-many)
             └── Subject      (one-to-many)
```

### Model Summary

| Model | Key Fields |
|---|---|
| `StudentProfile` | user, full_name, email |
| `GradingSystem` | student, name, scale_type, maximum_grade_point, is_active |
| `GradeScale` | grading_system, grade, minimum_marks, maximum_marks, grade_point |
| `Semester` | student, semester_number, academic_year, gpa, total_credits |
| `Subject` | semester, subject_code, subject_name, credits, marks, grade, grade_point |

### SQLite (Development)
Zero configuration — SQLite file is created automatically on first `migrate`.

### PostgreSQL (Production)
Set `DATABASE_URL` environment variable. The application detects it automatically and switches from SQLite to PostgreSQL. No code changes required.

---

## Running Tests

```bash
# Run all tests
python manage.py test calculator

# Run with verbosity
python manage.py test calculator --verbosity=2
```

### Test Coverage

| Test Suite | Cases | What is tested |
|---|:---:|---|
| Grade Conversion | 14 | All grades S/A/B/C/D/E/RA, boundaries, invalid input |
| GPA Calculation | 6 | Single subject, multiple subjects, RA exclusion, zero credits |
| CGPA Calculation | 5 | Single/multiple semesters, different credit loads |
| Percentage Formula | 3 | AU percentage conversion formula |
| Target CGPA | 5 | Achievable, impossible, already above target, zero credits |
| Authentication | 4 | Register, login, logout, dashboard access control |
| Data Isolation | 2 | User A cannot access User B's semesters |
| Public Calculators | 4 | Anonymous access to all calculators |
| **Total** | **43** | |

---

## Deployment — Railway

Railway provides free cloud hosting with a managed PostgreSQL database — no credit card required for the free tier.

### Step 1 — Push to GitHub

```bash
git init
git add .
git commit -m "feat: initial production release"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/gpa-cgpa-calculator.git
git push -u origin main
```

### Step 2 — Create Railway project

1. Go to **https://railway.app** → sign up with GitHub
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your `gpa-cgpa-calculator` repository

### Step 3 — Add PostgreSQL

1. In your Railway project, click **"+ New"**
2. Select **"Database"** → **"Add PostgreSQL"**
3. Railway automatically injects `DATABASE_URL` into your service

### Step 4 — Set environment variables

Railway dashboard → your service → **Variables** tab:

| Variable | Value |
|---|---|
| `SECRET_KEY` | Output of the `get_random_secret_key()` command above |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `your-app-name.railway.app` |

> `DATABASE_URL` is set automatically by Railway — do not add it manually.

### Step 5 — Set build and start commands

Railway dashboard → your service → **Settings** tab:

**Build Command:**
```
pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate
```

**Start Command:**
```
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2
```

### Step 6 — Deploy

Click **Deploy**. Build takes approximately 2–3 minutes.

### Step 7 — Create admin user

Railway dashboard → your service → **Shell** tab:
```bash
python manage.py createsuperuser
```

Your application is now live at `https://your-app-name.railway.app` 🎉

---

## Security

| Security Measure | Implementation |
|---|---|
| CSRF Protection | Django middleware — all POST forms protected |
| Password Hashing | Django's `PBKDF2PasswordHasher` (SHA-256) |
| Data Isolation | All querysets filtered by `student=request.user` |
| Login Required | `@login_required` decorator on all private views |
| Object-Level Auth | `get_object_or_404(Model, pk=pk, student=request.user)` |
| Secure Cookies | `SESSION_COOKIE_SECURE` and `CSRF_COOKIE_SECURE` in production |
| No Secret Leaks | All secrets via environment variables, `.env` in `.gitignore` |
| XSS Prevention | Django template auto-escaping on all outputs |
| Clickjacking | `X_FRAME_OPTIONS = 'DENY'` in production |

---

## API Endpoints

| Method | URL | Description | Auth |
|---|---|---|:---:|
| `GET` | `/` | Home / landing page | No |
| `GET/POST` | `/gpa/` | GPA Calculator | No |
| `GET/POST` | `/cgpa/` | CGPA Calculator | No |
| `GET/POST` | `/target-cgpa/` | Target CGPA Calculator | No |
| `GET/POST` | `/grading-system/` | Grading System config | Yes |
| `GET` | `/dashboard/` | Student dashboard | Yes |
| `GET/POST` | `/semester/add/` | Add semester | Yes |
| `GET` | `/semester/<id>/` | Semester detail | Yes |
| `GET/POST` | `/semester/<id>/edit/` | Edit semester | Yes |
| `POST` | `/semester/<id>/delete/` | Delete semester | Yes |
| `GET/POST` | `/semester/<id>/subjects/` | Manage subjects | Yes |
| `POST` | `/subject/<id>/delete/` | Delete subject | Yes |
| `GET` | `/register/` | Registration | No |
| `GET/POST` | `/login/` | Login | No |
| `GET` | `/logout/` | Logout | Yes |
| `GET` | `/api/grade-lookup/` | JSON grade lookup | No |
| `GET` | `/admin/` | Django Admin | Superuser |

---

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'feat: add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

### Commit Message Convention

```
feat:     New feature
fix:      Bug fix
docs:     Documentation only
style:    Formatting, no logic change
refactor: Code change that neither fixes a bug nor adds a feature
test:     Adding or updating tests
chore:    Build process or auxiliary tool changes
```

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- [Django](https://djangoproject.com) — The web framework for perfectionists with deadlines
- [Bootstrap](https://getbootstrap.com) — Frontend UI framework
- [Chart.js](https://chartjs.org) — JavaScript charting library
- [Railway](https://railway.app) — Cloud deployment platform
- Annamalai University — Faculty of Engineering & Technology grading regulations

---

<div align="center">

**Built with ❤️ for Annamalai University students**

</div>
