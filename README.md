# NiroxCode

[![Deploy](https://github.com/AmarnathSharma10/NiroxCode/actions/workflows/deploy.yml/badge.svg)](https://github.com/AmarnathSharma10/NiroxCode/actions/workflows/deploy.yml)

An online coding platform and judge built with Django. Users write, compile, run and submit code in the browser, and solutions are checked against test cases.

**Live:** https://niroxcode.pro

## Table of Contents

- [Features](#features)
- [Tech stack](#tech-stack)
- [Architecture](#architecture)
- [Project structure](#project-structure)
- [Running locally](#running-locally)
- [Configuration](#configuration)
- [Deployment and CI/CD](#deployment-and-cicd)
- [Roadmap](#roadmap)

## Features

- Supports multiple languages: Java, Python, C and C++
- Easy administration: problems and test cases are added or removed through the Django admin
- When a submission is rejected, the user can see the test case input, the expected output and their program's output
- User accounts and authentication

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Django 5, gunicorn |
| Frontend | HTML, CSS, vanilla JavaScript |
| Database | SQLite |
| Static files | WhiteNoise |
| Containers | Docker, Docker Compose |
| Reverse proxy | Caddy |
| Edge | Cloudflare |
| CI/CD | GitHub Actions, Docker Hub |

## Architecture

```
Browser
   |  HTTPS
   v
Cloudflare          TLS termination, bot protection, hides the server IP in DNS
   |  HTTPS (Full strict, Cloudflare Origin Certificate)
   v
VPS :443 --> Caddy  accepts only Cloudflare IP ranges, everything else gets 403
               |  reverse proxy over a private Docker network
               v
            Django + gunicorn   (no port published to the host)
               |
               v
            Docker volume       SQLite database persists across deploys
```

Only Caddy publishes ports (80 and 443). The Django container is reachable only through Caddy.

## Project structure

The repository root holds the Django project in `Main/`, plus the CI configuration:

```
.github/workflows/deploy.yml    CI/CD pipeline
Main/                           Django project root (Dockerfile and manage.py live here)
  Main/                         Project package: settings, urls, wsgi, asgi
  accounts/                     User accounts app (models, views, templates, migrations)
  home/                         Core app: problems, submissions, judging
  codes/                        Submitted code is stored here at run time
  inputs/ outputs/              Input and output files used during code execution
  static/                       Static assets
  Dockerfile
  manage.py
  requirements.txt
```

The image includes a JDK (17), `gcc` and `g++`, because submissions are compiled and executed by the application.

## Running locally

Clone the repository first:

```bash
git clone https://github.com/AmarnathSharma10/NiroxCode.git
cd NiroxCode/Main
```

### With Docker

Prerequisite: Docker.

```bash
docker build -t niroxcode:local .

docker run --rm -p 8000:8000 \
  -e DEBUG=True \
  -e ALLOWED_HOSTS=localhost,127.0.0.1 \
  -e DB_PATH=/niroxcode/data/db.sqlite3 \
  -v niroxcode_data:/niroxcode/data \
  niroxcode:local
```

Open http://localhost:8000. Migrations run automatically on start. To use the admin, create a superuser in a second terminal:

```bash
docker exec -it $(docker ps -q --filter ancestor=niroxcode:local) python manage.py createsuperuser
```

### Without Docker

Prerequisites: Python 3.11+, JDK 17, `gcc` and `g++`.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export DEBUG=True
export ALLOWED_HOSTS=localhost,127.0.0.1

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Configuration

Settings are read from environment variables, so no secrets live in the repository.

| Variable | Purpose | Default |
|---|---|---|
| `SECRET_KEY` | Django secret key | insecure development value |
| `DEBUG` | Debug mode | `True` |
| `ALLOWED_HOSTS` | Comma-separated host names | empty |
| `CSRF_TRUSTED_ORIGINS` | Comma-separated origins, with `https://` | empty |
| `DB_PATH` | Path to the SQLite file | `db.sqlite3` in the project folder |

In production these are set in a `.env` file on the server (never committed). Always set a real `SECRET_KEY` outside local development.

## Deployment and CI/CD

Pushing to `main` deploys the site automatically:

1. GitHub Actions checks out the code and builds the Docker image, using layer caching
2. The image is pushed to Docker Hub with two tags: `latest` and the commit SHA (the SHA tag allows an easy rollback)
3. The workflow connects to the server over SSH with a dedicated deploy key, runs `docker compose pull` and `docker compose up -d`, then checks that the app container is running. The run fails if it is not

Any branch can also be deployed from the Actions tab (**Run workflow**), which is useful for checking a pull request before merging.

Credentials (Docker Hub token, SSH key, server address) are stored as GitHub Actions secrets.

**Server setup:** Ubuntu VPS with Docker Compose running two services, `web` (Django and gunicorn) and `caddy`. The SQLite database lives on a named Docker volume, so it survives redeploys. The server uses a non-root user, key-only SSH and a default-deny firewall.

A detailed write-up of the deployment, including the problems I ran into and how I solved them, is in [DEPLOYMENT.md](DEPLOYMENT.md).

## Roadmap

- Automated nightly database backups, copied off the server
- Run `DEBUG=False` in production
- Add a test stage to the pipeline before the image is built
- Staging environment with its own database
