# FROM alpine:3.19

# RUN echo "http://dl-cdn.alpinelinux.org/alpine/v3.9/main" >> /etc/apk/repositories && \
#     echo "http://dl-cdn.alpinelinux.org/alpine/v3.9/community" >> /etc/apk/repositories && \
#     apk add --update curl zip python3 py3-pip wget mongodb mongodb-tools aws-cli && \
#     wget https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem -O /tmp/global-bundle.pem && \
#     curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/mac/sessionmanager-bundle.zip" -o "sessionmanager-bundle.zip" && \
#     unzip sessionmanager-bundle.zip && \
#     ./sessionmanager-bundle/install -i /usr/local/sessionmanagerplugin -b /usr/local/bin/session-manager-plugin

# WORKDIR app

# COPY requirements.txt  .

# RUN  pip install -r requirements.txt --break-system-packages

# COPY . .

# CMD ["python", "main.py"]

FROM mongo:7

RUN apt-get update && \
    apt-get install -y gnupg zip curl wget python3 python3-pip mysql-client redis && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_arm64/session-manager-plugin.deb" -o "session-manager-plugin.deb" && \
    dpkg -i session-manager-plugin.deb && \
    wget https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem -O /tmp/global-bundle.pem

WORKDIR app

COPY requirements.txt  .

RUN  pip3 install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]