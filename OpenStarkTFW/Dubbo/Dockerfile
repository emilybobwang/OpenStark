FROM maven:3-openjdk-8
RUN mkdir /source && wget https://github.com/apache/dubbo-admin/archive/0.2.0.zip && unzip -q 0.2.0.zip -d /source
WORKDIR /source/dubbo-admin-0.2.0
RUN sed -i 's/https:\/\/repository.apache.org\/content\/repositories\/snapshots/https:\/\/maven.aliyun.com\/repository\/apache-snapshots/g' pom.xml
RUN ls dubbo-admin-distribution && sed -i 's/127.0.0.1/zookeeper.server/g' dubbo-admin-server/src/main/resources/application.properties
RUN mkdir -p ~/.m2 && printf '<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"\n xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0\n https://maven.apache.org/xsd/settings-1.0.0.xsd">\n <mirrors>\n <mirror>\n <id>aliyunmaven</id>\n <mirrorOf>*</mirrorOf>\n <name>阿里云公共仓库</name>\n <url>https://maven.aliyun.com/repository/public</url>\n </mirror>\n </mirrors>\n </settings>' > ~/.m2/settings.xml
RUN printf 'registry=https://registry.npm.taobao.org' >> ~/.npmrc
RUN mvn --batch-mode clean package -Dmaven.test.skip=true

FROM openjdk:8-jre
LABEL maintainer="dev@dubbo.apache.org"
COPY --from=0 /source/dubbo-admin-0.2.0/dubbo-admin-distribution/target/dubbo-admin-0.2.0.jar /app.jar
RUN printf '#!/bin/bash\nif [ -e /etc/host ];then cat /etc/host >> /etc/hosts;fi\njava -XX:+UnlockExperimentalVMOptions -XX:+UseCGroupMemoryLimitForHeap -Djava.security.egd=file:/dev/./urandom -jar /app.jar' > /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
EXPOSE 8080
