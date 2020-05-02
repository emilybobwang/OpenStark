FROM python

VOLUME /data
WORKDIR /data

COPY ./requirements.txt /data/requirements.txt
RUN cp -f /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && pip install -U -r /data/requirements.txt