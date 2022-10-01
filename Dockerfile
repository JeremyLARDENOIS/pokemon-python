FROM python:3.9-alpine

COPY server.py .
COPY lib lib

CMD ["python3", "server.py"]

EXPOSE 3333

