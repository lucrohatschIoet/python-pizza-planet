FROM python:3.10-slim-bullseye
ENV PYTHONUNBUFFERED=1

WORKDIR /src

COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install --upgrade pip wheel\
    && pip install -r requirements.txt
COPY app/ app/
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app.__init__:flask_app"]