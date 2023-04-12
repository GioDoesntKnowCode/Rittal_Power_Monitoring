#!/bin/bash
# ssh -R <port>:localhost:80 <user>@localhost
# made to run on MAC using osascript || Can also just run ssh -R <port>:localhost:80 <user>@<machine_IP> on windows to do the same thing
# osascript -e 'tell application "Terminal" to do script "ssh -R <port>:localhost:80 <user>@<machine_IP>"'

username="$1"
ipaddr="$2"

osascript -e 'tell application "Terminal" to do script "ssh -L 8080:192.168.0.200:80 '"$username@$ipaddr"'"'
