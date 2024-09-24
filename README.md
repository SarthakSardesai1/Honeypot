# Honeypot

pip3 install -r requirements.txt

create key:--- 
ssh-keygen -t rsa -b 2048 -f server.key

Run:-- 
python3 main.py --ssh-port 2222 --http-port 8000 
