FROM python:2

LABEL maintainer="Graz<hcjonline@gmail.com>"

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /usr/src/app/ssshare

CMD [ "python", "quickstart.py" ]
