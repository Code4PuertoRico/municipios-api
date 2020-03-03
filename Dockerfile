FROM python:3.7

WORKDIR /app

COPY requirements.txt  /app

RUN pip install -r requirements.txt

COPY api.py data utils /app/

CMD ["gunicorn", "--workers", "2", "api:app"]