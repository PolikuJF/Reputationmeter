FROM python:3.11-slim

WORKDIR /app

<<<<<<< HEAD
RUN apt-get update \
    && apt-get install -y --no-install-recommends firefox-esr ca-certificates \
    && rm -rf /var/lib/apt/lists/*

=======
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

<<<<<<< HEAD
RUN mkdir -p /app/logs /app/app/ParserReviews/csv

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
=======
RUN mkdir -p /app/logs

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
>>>>>>> 7f59b0e0a19afe8eb36a3cf6a5aec9d24fe8e7b1
