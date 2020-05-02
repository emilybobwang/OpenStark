#!/bin/bash
# Java Environment Path
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export JRE_HOME=${JAVA_HOME}/jre
export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
export PATH=${JAVA_HOME}/bin:$PATH
export GRADLE_HOME=/usr/local/gradle-$GRADLE_VERSION
export PATH=$GRADLE_HOME/bin:$PATH

export NODE_REGISTRY=https://npm.taobao.org/mirrors/node
export CHROMEDRIVER_CDNURL=http://npm.taobao.org/mirrors/chromedriver/
export CHROMEDRIVER_VERSION=`curl -L https://npm.taobao.org/mirrors/chromedriver/LATEST_RELEASE`
export ELECTRON_MIRROR=https://npm.taobao.org/mirrors/electron/
export DISPLAY=':1'
export NODE_IN_DOCKER=1
export ROOTPASSWORD=macaca

# Run sshd
/usr/sbin/sshd

macaca -v
macaca doctor

/startup.sh  &

# Run Macaca In Background
macaca server --verbose
