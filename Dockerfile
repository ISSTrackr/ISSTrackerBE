FROM python:3.8.5-alpine

# Environment
ENV REDISHOST="localhost"
ENV REDISPW="password"

# Init
WORKDIR /usr/src/app
COPY . .
RUN rm dump.rdb

# Setup
RUN apk update && apk add --no-cache build-base libxml2-dev libxslt-dev
RUN pip install -r requirements.txt
EXPOSE 5000

# Finalize
ENTRYPOINT [ "python", "application.py" ]