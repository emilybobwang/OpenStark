FROM maven:3-jdk-8
RUN git clone --depth 1 --single-branch -b develop https://github.com/apache/incubator-dubbo-ops.git /source
WORKDIR /source
RUN git rev-parse HEAD
RUN ls dubbo-admin-distribution && sed -i 's/127.0.0.1/zookeeper.server/g' dubbo-admin-server/src/main/resources/application.properties
RUN mvn clean package -Dmaven.test.skip=true
RUN printf '#!/bin/bash\nif [ -e /etc/host ];then cat /etc/host >> /etc/hosts;fi\njava -Djava.security.egd=file:/dev/./urandom -jar /source/dubbo-admin-distribution/target/dubbo-admin-0.1.jar' > /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
EXPOSE 8080
