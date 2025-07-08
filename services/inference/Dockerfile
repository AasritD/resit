FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

COPY app/ ./app
WORKDIR /app/app
EXPOSE 8000
CMD ["bash","-lc","python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"]
