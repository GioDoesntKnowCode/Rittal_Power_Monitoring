
read -p "Enter username: " username
read -p "Enter ip address: " ipaddr


bash ./local_connection.sh  "$username" "$ipaddr" # Recieve Rittal Website on your machine
bash ./host_connection.sh  "$username" "$ipaddr" # Forward Rittal Website to your machine
