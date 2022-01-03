#!/bin/bash

<< 'MULTILINE-COMMENT'

You have just cloned this repo into a fresh ubuntu vm.
Before running this script, here is a checklist:

- Install npm 8.1.2. This should correspond with node 16.13.1
- Install docker 20.10.7 or higher.
- Install docker-compose 1.29.2 or higher. (Technically not needed but just easier to use it imo).
- Install nginx 1.18.0 or higher.
- Install certbot from snap store.
- 
- Use certbot to prepare certificates. Place them inside:
	ssl_certificate /etc/letsencrypt/live/mcss.utmrobotics.com/fullchain.pem;
	ssl_certificate_key /etc/letsencrypt/live/mcss.utmrobotics.com/privkey.pem;

- Have .env files ready in server/ and deerhunt/
- Change FLASK_ENV to 'production' in server/Dockerfile
- Make sure port 80 and 443 are open for nginx.
- Make sure port 5000 is not in use.
- Run sudo apt update and sudo apt upgrade before.


MULTILINE-COMMENT


cd deerhunt/
printf "Building frontend static files..."
npm run build
printf "frontend built. Copying static files to nginx /var/www/html/\n\n"
sudo rm -r  /var/www/html/*
cd build/
sudo cp -r * /var/www/html/

printf "Copying our deerhunt nginx.conf file to /etc/nginx/nginx.conf\n"
cd ../../nginx/
sudo cp nginx.conf /etc/nginx/

cd ..
printf "Starting flask docker container...\n"
sudo docker-compose up -d

printf "Restarting nginx. If fails, check /var/log/nginx/error.log\n"
sudo systemctl restart nginx

printf "\nHosted\n"
