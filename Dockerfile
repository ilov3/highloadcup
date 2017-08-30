FROM python:3.6

WORKDIR /root

COPY dist/hlcup-0.1.tar.gz /root/hlcup-0.1.tar.gz

RUN pip install /root/hlcup-0.1.tar.gz

ENV JAPRONTO_PORT 80

ENV JAPRONTO_HOST 0.0.0.0

ENV WORKER_NUM 8

ENV SMALL_DATA 0

ENV INMEMORY 0

ENV LEVEL DEBUG

EXPOSE 80

COPY run.sh /root/run.sh

CMD sh run.sh