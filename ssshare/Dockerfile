FROM python:3

LABEL maintainer="Graz<hcjonline@gmail.com>"

RUN set -ex \
      && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
      && echo "Asia/Shanghai" > /etc/timezone \

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --upgrade pip \
      && pip install \
                --index-url https://mirrors.aliyun.com/pypi/simple \
                --no-cache-dir \
                -r requirements.txt

COPY . .

CMD [ "python", "quickstart.py" ]
