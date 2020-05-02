#!/bin/bash

apt-get update --fix-missing && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
( sleep 4 && while [ 1 ]; do sleep 1; echo y; done ) | apt-get install -y --no-install-recommends ca-certificates curl git openjdk-8-jdk xvfb libxtst6 libgtk2.0 libgconf2-dev libasound2 libxss1 libnss3 xauth libnotify-dev make fonts-droid-fallback ttf-wqy-zenhei ttf-wqy-microhei fonts-arphic-ukai fonts-arphic-uming fonts-tlwg-garuda
( sleep 4 && while [ 1 ]; do sleep 1; echo y; done ) | apt-get install -y --no-install-recommends qemu-kvm qemu-utils bridge-utils dnsmasq uml-utilities iptables
( sleep 4 && while [ 1 ]; do sleep 1; echo y; done ) | apt-get install -y --no-install-recommends build-essential vim zip unzip wget bzip2 openssh-server socat
( sleep 4 && while [ 1 ]; do sleep 1; echo y; done ) | apt-get install -y --no-install-recommends software-properties-common
( sleep 4 && while [ 1 ]; do sleep 1; echo y; done ) | apt-get install -y --no-install-recommends net-tools iputils-ping dnsutils
( sleep 4 && while [ 1 ]; do sleep 1; echo y; done ) | apt-get install -y --no-install-recommends python-dev python-pip libappindicator3-1
( sleep 4 && while [ 1 ]; do sleep 1; echo y; done ) | apt-get install -y --no-install-recommends apt-utils usbutils locales udev libatk-bridge2.0-0
( sleep 4 && while [ 1 ]; do sleep 1; echo y; done ) | apt-get install -y --no-install-recommends gconf-service libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 fonts-liberation libappindicator1 lsb-release xdg-utils

# Install packages needed for android sdk tools
dpkg --add-architecture i386
( sleep 4 && while [ 1 ]; do sleep 1; echo y; done ) | apt-get install -y --no-install-recommends libstdc++6:i386 libgcc1:i386 zlib1g:i386 libncurses5:i386
apt-get autoremove -y && apt-get clean -y

curl -o google-chrome-stable_current_amd64.deb -L https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable_current_amd64.deb && rm -f google-chrome-stable_current_amd64.deb

# Java Environment Path
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export JRE_HOME=${JAVA_HOME}/jre
export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
export PATH=${JAVA_HOME}/bin:$PATH

# Install Android SDK
export ANDROID_HOME=/opt/android-sdk-linux
export ANDROID_NDK_HOME=$ANDROID_HOME/android-ndk-r14b
export PATH=$PATH:$ANDROID_HOME/tools/:$ANDROID_HOME/platform-tools:$ANDROID_NDK_HOME

curl -o android-sdk.tgz https://dl.google.com/android/android-sdk_r24.4.1-linux.tgz && tar -C /opt -zxvf android-sdk.tgz > /dev/null
curl -o ndk-bundle.zip https://dl.google.com/android/repository/android-ndk-r14b-linux-x86_64.zip && unzip ndk-bundle.zip -d $ANDROID_HOME > /dev/null

rm -f android-sdk.tgz && rm -f ndk-bundle.zip
mkdir "$ANDROID_HOME/licenses" || true
echo -e "\n8933bad161af4178b1185d1a37fbf41ea5269c55" > "$ANDROID_HOME/licenses/android-sdk-license"
echo -e "\d56f5187479451eabf01fb78af6dfcb131a6481e" >> "$ANDROID_HOME/licenses/android-sdk-license"
echo -e "\n84831b9409646a918e30573bab4c9c91346d8abd" > "$ANDROID_HOME/licenses/android-sdk-preview-license"

( sleep 4 && while [ 1 ]; do sleep 1; echo y; done ) | android update sdk --no-ui --force -a --filter platform-tool,android-25,android-26,android-27,build-tools-27.0.3,extra-android-support,extra-android-m2repository,extra-google-m2repository
( sleep 4 && while [ 1 ]; do sleep 1; echo y; done ) | android update adb

which adb
which android

# Gradle 5.0
GRADLE_VERSION=5.0
export GRADLE_HOME=/usr/local/gradle-$GRADLE_VERSION
export PATH=$GRADLE_HOME/bin:$PATH

curl -o gradle-$GRADLE_VERSION-bin.zip -L https://services.gradle.org/distributions/gradle-$GRADLE_VERSION-bin.zip
unzip gradle-$GRADLE_VERSION-bin.zip -d /usr/local > /dev/null
rm -f gradle-$GRADLE_VERSION-bin.zip

# Node.js
NODE_VERSION=11.3.0
export NODE_REGISTRY=https://npm.taobao.org/mirrors/node
export CHROMEDRIVER_CDNURL=http://npm.taobao.org/mirrors/chromedriver/
export ELECTRON_MIRROR=https://npm.taobao.org/mirrors/electron/
export CHROMEDRIVER_VERSION=`curl -L https://npm.taobao.org/mirrors/chromedriver/LATEST_RELEASE`
export DISPLAY=':1'
export NODE_IN_DOCKER=1
export ROOTPASSWORD=macaca

curl -SLO "$NODE_REGISTRY/v$NODE_VERSION/node-v$NODE_VERSION-linux-x64.tar.gz"
tar -xzf "node-v$NODE_VERSION-linux-x64.tar.gz" -C /usr/local --strip-components=1
rm -f "node-v$NODE_VERSION-linux-x64.tar.gz"

# Run sshd
mkdir /var/run/sshd && \
echo "root:$ROOTPASSWORD" | chpasswd && \
sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd && \
echo "export VISIBLE=now" >> /etc/profile

npm install -g cnpm --registry=https://registry.npm.taobao.org
cnpm i -g macaca-cli
cnpm i -g macaca-android macaca-chrome macaca-chromedriver macaca-electron macaca-puppeteer
macaca -v
macaca doctor
