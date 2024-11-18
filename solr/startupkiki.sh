#!/bin/bash

CONTAINER_NAME="wikiwar_solr"
COLLECTION_NAME="wikiwar"
DATA_FILE="output.json"
SCHEMA_FILE="schema.json"

# Verify if the container is already running
if [ "$(sudo docker ps -q -f name=$CONTAINER_NAME)" ]; then  
    sudo docker stop $CONTAINER_NAME
    sudo docker rm $CONTAINER_NAME
fi

# Run the Solr container
sudo docker run -p 8983:8983 --name $CONTAINER_NAME -v "$(pwd):/data" -d solr:9 solr-precreate $COLLECTION_NAME

sudo sleep 5

#Schema configuration (Later) with API 
sudo curl -X POST -H 'Content-type:application/json' \
    --data-binary "@$SCHEMA_FILE" \
    http://localhost:8983/solr/$COLLECTION_NAME/schema


#Populate the collection
sudo docker exec $CONTAINER_NAME bin/solr post -c $COLLECTION_NAME /data/$DATA_FILE