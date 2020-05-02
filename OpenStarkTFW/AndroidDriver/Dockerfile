FROM dorowu/ubuntu-desktop-lxde-vnc:bionic

# Expose ADB, Macaca and VNC ports
EXPOSE 22
EXPOSE 80
EXPOSE 3456
EXPOSE 5900

WORKDIR /root
ENV DEBIAN_FRONTEND=noninteractive

ADD rootfs.tar.xz /

COPY sources.list /etc/apt/sources.list

VOLUME /data

ADD initEnv.sh /initEnv.sh
ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN chmod +x /initEnv.sh && /initEnv.sh
ENTRYPOINT ["/entrypoint.sh"]