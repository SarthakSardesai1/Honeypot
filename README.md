# Honeypot
create key 
ssh-keygen -t rsa -b 2048 -f server.key
python3 main.py -a 0.0.0.0 -p 22 --ssh -u admin -p admin --tarpit

