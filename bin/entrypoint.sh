#!/bin/bash

# Define the number of clients
num_clients=$1

# Start of the compose file
cat <<EOF > docker-compose.yml
version: '3.4'

services:
  continuous_double_auction:
    image: project
    build: .
    ports:
      - '8082:8090'
    networks:
      exchange:
        ipv4_address: 10.10.0.2
EOF

# Add clients
for ((i=0; i<num_clients; i++))
do
    cat <<EOF >> docker-compose.yml
  client_$i:
    image: project
    ports:
      - '$((8083+i)):8090'
    env_file:
       - 'variables.env'
    depends_on:
      - continuous_double_auction
    networks:
      exchange:
        ipv4_address: 10.10.0.$((3+i))
EOF
done

# Add networks
cat <<EOF >> docker-compose.yml
networks:
  exchange:
    ipam:
      config:
        - subnet: 10.10.0.0/24
EOF

docker-compose up