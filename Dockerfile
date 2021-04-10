FROM ubuntu:20.04

RUN apt update && apt install -y python3 python3-pip \
&& pip3 install flask bs4 lxml

COPY . /hackaday-lite

EXPOSE 5000
ENV FLASK_APP=/hackaday-lite/app
ENV FLASK_ENV=development

CMD flask run --host=0.0.0.0

