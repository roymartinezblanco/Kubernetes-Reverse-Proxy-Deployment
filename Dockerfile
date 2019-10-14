FROM python:alpine3.7
COPY /app/server.py server.py
COPY requirements.txt requirements.txt
COPY config.yaml config.yaml
RUN pip install -r requirements.txt
EXPOSE 8081
CMD python ./app.py