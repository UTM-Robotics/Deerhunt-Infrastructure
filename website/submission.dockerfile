FROM python:3.7-alpine

RUN mkdir /src

COPY . /src

WORKDIR /src/server

CMD ["/src/server/run.sh", "8888"]
