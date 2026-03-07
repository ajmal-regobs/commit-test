FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV APP_PORT=3333
EXPOSE 3333

CMD ["gunicorn", "--bind", "0.0.0.0:3333", "main:app"]
