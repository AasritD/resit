FROM python:3.10-slim

WORKDIR /mlflow    # or /app for training service

# Use pip install flags: no cache, retries, increased timeout
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir \
      --default-timeout=100 \
      --retries=5 \
      -r requirements.txt

VOLUME ["/mlruns"] 

EXPOSE 5000       

ENTRYPOINT ["mlflow", "server", \
  "--backend-store-uri", "sqlite:///mlflow.db", \
  "--default-artifact-root", "/mlruns", \
  "--host", "0.0.0.0", \
  "--port", "5000"]
