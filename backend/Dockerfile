FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY ./extractor .

RUN python manage.py migrate

COPY entry.sh .
RUN chmod 777 entry.sh
ENTRYPOINT ["./entry.sh"]
