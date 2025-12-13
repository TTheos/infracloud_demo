FROM python
ENV TZ=Europe/Brussels
WORKDIR /home/myapp
RUN pip install --no-cache-dir --progress-bar off flask requests bcrypt
COPY ./static ./static
COPY ./templates ./templates
COPY sample_app.py ./sample_app.py
EXPOSE 5555
CMD python3 sample_app.py
