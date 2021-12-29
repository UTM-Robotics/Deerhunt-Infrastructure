FROM python:3.9-slim-buster

WORKDIR /server

# Change to 'production' when running for real.
ENV FLASK_ENV=development

# Must be set to allow python output to buffer through
ENV PYTHONUNBUFFERED=1

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["./gunicorn.sh"]
