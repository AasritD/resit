# services/core_project/Dockerfile

FROM python:3.10-slim

# 1. Use /app as the project root
WORKDIR /app

# 2. Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy your Django project from the inner "app/" folder
COPY app/ .

# 4. Run Gunicorn against the now‐flat core_project package
CMD ["gunicorn", "core_project.wsgi:application", "--bind", "0.0.0.0:8000"]
