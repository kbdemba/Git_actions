#!/bin/bash


# Also docker build -t sso_example .
docker network create -d bridge mybridge

docker run -d -v /db/index256:/db -e "ANN_INDEX_LENGTH=256" \
    --network=mybridge --name nn_search nn_search

docker run -d --network=mybridge --name=facerec cachengo/facerec:latest

docker run -it -p 5000:5000 -v /db/sso:/db -e "NN_SEARCH_ADDRESS=nn_search:5000" \
  -e "FACEREC_ADDRESS=facerec:5000" --network=mybridge --name sso sso_example