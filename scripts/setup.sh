#!/usr/bin/env sh

echo 'Start building image!'

FLAGS=()

for arg in "$@"
do
    FLAGS+=("$1")
    shift
done

docker-compose build --no-cache --force-rm ${FLAGS[*]}
