FROM python:3.8-alpine

RUN pip install --no-cache-dir flask

WORKDIR /app
COPY app.py /app/app.py

EXPOSE 8080
CMD ["python3", "/app/app.py"]

