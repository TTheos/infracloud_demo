#!/bin/bash

# Clean previous build dir
rm -rf tempdir
mkdir tempdir
mkdir tempdir/templates
mkdir tempdir/static

# Copy app files
cp sample_app.py tempdir/.
cp -r templates/* tempdir/templates/.
cp -r static/* tempdir/static/.

# Create Dockerfile
cd tempdir

echo "FROM python" > Dockerfile
echo "ENV TZ=Europe/Brussels" >> Dockerfile
echo "WORKDIR /home/myapp" >> Dockerfile
echo "RUN pip install --no-cache-dir --progress-bar off flask requests bcrypt" >> Dockerfile
echo "COPY ./static ./static" >> Dockerfile
echo "COPY ./templates ./templates" >> Dockerfile
echo "COPY sample_app.py ./sample_app.py" >> Dockerfile
echo "EXPOSE 5555" >> Dockerfile
echo "CMD python3 sample_app.py" >> Dockerfile

# Build image
docker build -t sampleapp .

# Stop oude container als die bestaat
docker stop samplerunning 2>/dev/null
docker rm samplerunning 2>/dev/null

# Run nieuwe container
docker run -t -d -p 5555:5555 --name samplerunning sampleapp

# Toon status
docker ps -a
