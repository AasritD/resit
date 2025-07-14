# services/core_project/app/Dockerfile
FROM python:3.10-slim
WORKDIR /app

# 1) Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) Copy the entire Django project into /app
COPY . .

# 3) Expose port & declare entrypoint
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=core_project.settings
EXPOSE 8000
CMD ["gunicorn", "core_project.wsgi:application", "--bind", "0.0.0.0:8000"]
