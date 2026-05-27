# Breathe ESG - Tech Intern Assignment Prototype

Prerequisites
 - Python 3.10+
 - Node.js 18+ and npm (or `corepack`)
 - Git
 - Docker (optional, recommended for deployment)
 - PostgreSQL for production; SQLite is used for local development

Quick start (local development)

 Backend
 ```bash
 python -m venv .venv
 .venv\Scripts\activate   # Windows
 pip install -r requirements.txt
 cd backend
 python manage.py migrate
 python manage.py load_sample_data
 python manage.py create_demo_user
 python manage.py runserver
 ```

 Frontend
 ```bash
 cd frontend
 npm install
 npm start
 ```

 Demo credentials
 - Username: `demo_analyst`
 - Password: `demo1234`
 - Token: Fetch via GET `/api/demo-token/` on the deployed or local backend.

 Usage
 1. Start backend and frontend.
 2. Open the UI, paste the API token into the token input, and click `Set token`.
 3. Upload sample CSV files with the ingestion panel and select the source type.
 4. Approve or reject pending records in the review dashboard.

 Deployment
 - The repository contains `Dockerfile`, `docker-compose.yml`, `Procfile`, and `.env.example` for containerized runs.
 - Build and run the production image:
 ```bash
 docker build -t breathe-esg-assessment .
 docker run --rm -p 8000:8000 breathe-esg-assessment
 ```
 - Or use Docker Compose:
 ```bash
 docker compose up --build
 ```
 - Then open `http://localhost:8000`.
 - Live deployment: `https://breathe-esg-assessment.onrender.com/`
 - For container platforms such as Heroku or Render, connect a GitHub repository and use the included `Procfile` and Dockerfile.
 - Use `.env.example` to set `DJANGO_SECRET_KEY`, `DEBUG`, and `DJANGO_ALLOWED_HOSTS` in production.
 - If your local environment has Node but no npm, run `corepack enable` before frontend installation.

CI / Cloud deployment
 - A GitHub Actions workflow runs a build validation path, including frontend build and Django `manage.py check`.
 - Push this repository to GitHub and connect it to your cloud provider to deploy the app.

Files of interest
 - `MODEL.md`, `DECISIONS.md`, `TRADEOFFS.md`, `SOURCES.md` — documentation required by the assignment.
>>>>>>> f1d192f (Initial commit: assessment project ready for deployment)
