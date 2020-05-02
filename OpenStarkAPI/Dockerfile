FROM python
USER root
VOLUME /data
WORKDIR /data
COPY . /data

RUN if [ ! -e /data/static/files/jd-core-java-1.2.jar ];then mkdir -p /data/static/files; curl -L http://clojars.org/repo/org/clojars/razum2um/jd-core-java/1.2/jd-core-java-1.2.jar > /data/static/files/jd-core-java-1.2.jar; fi && \
    apt-get update && apt-get install -y --no-install-recommends && \
    apt-get install -y default-jdk && \
	java -version
RUN apt-get install -y fonts-liberation fonts-droid-fallback ttf-wqy-zenhei ttf-wqy-microhei fonts-arphic-ukai fonts-arphic-uming fonts-tlwg-garuda
RUN cd /data && \
    pip3 install --upgrade pip && \
    pip3 install -r /data/requirements.txt && \
	ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
ENV NODE_VERSION=11.3.0 \
    NODE_REGISTRY=https://npm.taobao.org/mirrors/node
RUN curl -SLO "$NODE_REGISTRY/v$NODE_VERSION/node-v$NODE_VERSION-linux-x64.tar.gz" && \
    tar -xzf "node-v$NODE_VERSION-linux-x64.tar.gz" -C /usr/local --strip-components=1 && \
    rm -f "node-v$NODE_VERSION-linux-x64.tar.gz"
RUN npm install -g cnpm --registry=https://registry.npm.taobao.org && \
    cnpm i -g phantomjs-prebuilt

EXPOSE 9090
CMD /bin/bash -c 'python3 /data/app_server.py --monitor=${MONITOR} --port=9090 --log_file_prefix=/data/logs/openStark.log --log-file-max-size=10000000 --log-file-num-backups=3'