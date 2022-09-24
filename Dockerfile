FROM python:3.10-slim-bullseye
ENV PYTHONUNBUFFERED=1

WORKDIR /src

COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install --upgrade pip wheel\
    && pip install -r requirements.txt
COPY app/ app/
COPY seeder/ seeder/
COPY manage.py .
RUN python3 manage.py db init \
    && python3 manage.py db migrate \
    && python3 manage.py db upgrade \
    && python3 manage.py seed
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app.__init__:flask_app"]