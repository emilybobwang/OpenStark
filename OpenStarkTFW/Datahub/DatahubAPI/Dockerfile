FROM python
USER root
VOLUME /data
WORKDIR /data
COPY . /data
RUN /bin/bash -c 'cd /data && pip3 install --upgrade pip && pip3 install -r /data/requirements.txt && \
	ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime'
EXPOSE 9090
CMD /bin/bash -c 'python3 /data/app_server.py --monitor=on --port=9090 --log_file_prefix=/data/logs/datahub.log --log-file-max-size=10000000 --log-file-num-backups=3'