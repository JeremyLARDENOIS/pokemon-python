FROM python:3.9-alpine

COPY pokepy_server.py .
COPY lib lib

CMD ["python3", "pokepy_server.py"]

EXPOSE 3333

