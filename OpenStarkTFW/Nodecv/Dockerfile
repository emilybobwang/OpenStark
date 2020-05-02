FROM macacajs/nodecv

WORKDIR /root
RUN git clone https://github.com/macacajs/nodecv-server.git /nodecv-server

ENTRYPOINT ["/nodecv-server/entrypoint.sh"]