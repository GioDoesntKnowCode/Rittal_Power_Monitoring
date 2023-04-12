#!/bin/bash


username="$1"
ipaddr="$2"

# This script sets up the network connection automatically on MAC, can be done manually for other OS as well.

ssh -t -t "$username@$ipaddr" << EOF         # ssh username@remote_host << EOF  
ssh -R 8080:localhost:80 $username@$ipaddr  
EOF
# ssh -L <port>:<host_ip_A>:80 <user>@<machine_ip_C>