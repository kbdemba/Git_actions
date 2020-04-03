#!/bin/bash


docker build -t sso_example .
docker network create -d bridge mybridge

docker stop sso
docker rm sso
docker stop nn_search
docker rm nn_search
docker stop facerec
docker rm facerec


docker run -d -v /db/index256:/db -e "ANN_INDEX_LENGTH=256" \
    --network=mybridge --name nn_search cachengo/nn_search:2.0

docker run -d --network=mybridge --name=facerec cachengo/facerec:1.0

docker run -d -p 5000:5000 -v /db/sso:/db -e "NN_SEARCH_ADDRESS=nn_search:1323" \
  -e "FACEREC_ADDRESS=facerec:5000" --network=mybridge --name sso sso_example
