FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory inside the container
WORKDIR /app

# Install system dependencies (if any) and Python requirements
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Copy the Django project into the container
COPY app/ ./app

# Move into the Django project folder
WORKDIR /app/app

# Expose the port the app runs on
EXPOSE 8000

# Apply migrations and start the development server
CMD ["bash", "-c", "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"]
