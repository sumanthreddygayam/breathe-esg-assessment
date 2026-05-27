FROM node:20-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/package.json ./
RUN npm install --silent
COPY frontend ./
RUN npm run build

FROM python:3.10-slim AS backend
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY backend ./backend
COPY --from=frontend-build /app/frontend/build ./frontend/build
WORKDIR /app/backend
ENV DJANGO_SETTINGS_MODULE=backend.settings
RUN python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
