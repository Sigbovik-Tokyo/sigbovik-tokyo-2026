FROM python:3.14

RUN pip install Flask gunicorn

# install dependencies
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app
WORKDIR /app

ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app