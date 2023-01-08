#!/bin/sh

for arg in "$@"
do
    FLAGS+=("$1")
    shift
done

set -x

docker-compose up ${FLAGS[*]}
