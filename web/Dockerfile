FROM python:3.7-alpine

LABEL maintainer="Graz<hcjonline@gmail.com>"

ENV SERVER_PORT 5000

ARG BRANCH=master
ARG WORK=/usr/src/web

RUN set -ex \
      && echo -e "http://mirrors.aliyun.com/alpine/v3.10/main\nhttp://mirrors.aliyun.com/alpine/v3.10/community" > /etc/apk/repositories \
      && apk update \
      && apk add --no-cache --virtual .build-deps \
                      git \
      && apk add --no-cache \
                      libsodium

WORKDIR $WORK

COPY requirements.txt .

RUN set -ex \
      && pip install --upgrade pip \
      && pip install --no-cache-dir git+https://github.com/hcaijin/ssrspeedtest.git@$BRANCH \
      && pip install \
                --index-url https://mirrors.aliyun.com/pypi/simple \
                --no-cache-dir \
                -r requirements.txt

RUN apk del .build-deps

COPY . .

EXPOSE $SERVER_PORT

CMD [ "python", "run.py" ]
