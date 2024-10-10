FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install flask requests

EXPOSE 9090  

CMD ["python", "run.py"] 