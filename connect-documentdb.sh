#!/bin/bash

LOCAL_PORT=$1
USERNAME=$2
PASSWORD=$3

mongosh mongo --tls --host localhost:$LOCAL_PORT \
  --tlsCAFile /tmp/global-bundle.pem \
  --tlsAllowInvalidHostnames \
  --username $USERNAME \
  --password $PASSWORD
