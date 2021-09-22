FROM python:3-alpine

#build with
# docker build -t me2d.eu/cml:1.1 .

LABEL maintainer="me2d@me2d.eu"

WORKDIR /usr/src/app

RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi libffi-dev openssl-dev

RUN pip install --no-cache-dir paho-mqtt cherrypy PyJWT cryptography

RUN apk del .build-deps gcc musl-dev libffi libffi-dev openssl-dev

COPY . .

EXPOSE 8080 8090

CMD [ "python", "./main.py" ]
