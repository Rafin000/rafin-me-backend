###########
# Builder #
###########

# Pull ofiicial base image
FROM python:3.10-alpine as builder

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

###############
# Final Stage #
###############

# official base image
FROM python:3.10-alpine

RUN apk add --update make

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV production
ENV APP_SETTINGS project.config.ProductionConfig

# install dependencies
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# add app
COPY . /usr/src/app/

ENV PYTHONPATH /usr/src/app

# run gunicorn
EXPOSE 6000
CMD make prod
