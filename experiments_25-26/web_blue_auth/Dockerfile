FROM python:3.8-alpine

RUN pip install --no-cache-dir flask werkzeug

WORKDIR /app
COPY app.py /app/app.py
COPY templates /app/templates
COPY static /app/static

EXPOSE 8080
CMD ["python3", "/app/app.py"]
