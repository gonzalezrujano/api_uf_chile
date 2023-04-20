#!/usr/bin/env bash

while getopts 'e:' flag;
do
  case "${flag}" in
    e) 
      environment=${OPTARG}
      ;;
  esac
done

echo Levantando sistema para ${environment} environment

case $environment in
    dev-without-redis)
        docker compose --env-file ./instance/envs/micro.env \
        -f docker-compose.yml \
        up --build -d 
    ;;

    dev)
        docker compose --env-file ./instance/envs/micro.env \
        -f docker-compose.yml \
        -f docker-compose.redis.yml \
        up --build -d
    ;;

    *)
        echo -n "Environment not provided"
    ;;
esac
