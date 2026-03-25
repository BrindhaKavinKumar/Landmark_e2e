FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/
COPY queue/ queue/
COPY sample-files/ sample-files/

ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "app.main"]