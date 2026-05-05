# Full-Stack Task Manager — DevOps CI/CD Lab

A three-tier web application deployed with full CI/CD pipelines.

**Author:** YOUR_NAME  
**Student ID:** YOUR_ID

---

## Architecture

```
Frontend (HTML/JS + Nginx)  →  Backend API (Flask)  →  PostgreSQL
        ↑                              ↑
  Railway service             Railway service
         \                            /
          \____________ or ___________/
                Docker Compose on DigitalOcean
                (+ Nginx reverse proxy on port 80)
```

## Tech Stack

| Layer     | Technology              |
|-----------|-------------------------|
| Frontend  | HTML, CSS, JavaScript   |
| Backend   | Python, Flask, Flask-CORS |
| Database  | PostgreSQL              |
| CI        | GitHub Actions (pytest) |
| CD        | Railway.app / DigitalOcean Droplet |

## API Endpoints

| Method | Path              | Description        |
|--------|-------------------|--------------------|
| GET    | `/api/data`       | List all tasks     |
| POST   | `/api/data`       | Create a new task  |
| DELETE | `/api/data/<id>`  | Delete a task      |

## Running Locally

```bash
# Backend (needs PostgreSQL running)
cd backend
pip install -r requirements.txt
export DATABASE_URL=postgresql://admin:secret123@localhost/taskdb
python app.py

# Frontend (serves on port 8080)
cd frontend
docker build -t frontend .
docker run -p 8080:80 frontend
```

## Full stack with Docker Compose (DigitalOcean setup)

```bash
docker-compose up -d
# App available at http://localhost
```

## Running tests

```bash
cd backend
pip install -r requirements.txt
pytest --tb=short -v
```

## Deployment

### Railway
- Backend: set `DATABASE_URL` from Railway PostgreSQL service
- Frontend: set `VITE_API_URL=https://your-backend.up.railway.app`
- CI triggers automatically on every push to `main`

### DigitalOcean
- All 4 containers (postgres, backend, frontend, nginx) managed by `docker-compose.yml`
- CD pipeline: GitHub Actions → SSH → `git pull && docker-compose up -d --build`
- Add secrets: `SERVER_IP` and `SSH_PRIVATE_KEY` in GitHub repo settings
