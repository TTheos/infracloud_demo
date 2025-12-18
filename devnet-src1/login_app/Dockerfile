FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --progress-bar off -r requirements.txt

COPY . .

ENV PORT=5000
ENV DB_PATH=/data/user.db

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "flask_app_v2:app"]
