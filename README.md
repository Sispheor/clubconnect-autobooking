# Club connect autobooking script

Script used to book automatically a training on clubconnect.fr

## Usage

Build the image
```bash
docker build -t clubconnect-autobooking .
```

Run the image
```bash
docker run -it --rm --name clubconnect-autobooking \
-e "USERNAME=me@email.com" \
-e "PASSWORD=secret" \
-e "CLUB_ID=abcd1234" \
-e "TRAINING_NAME=BOXE ANGLAISE" \
clubconnect-autobooking
```

## Execute automatically via cronjob

Script to execute
```bash
#!/bin/bash
docker stop clubconnect-autobooking || true && docker rm clubconnect-autobooking || true

docker run -it --rm --name clubconnect-autobooking \
-e "USERNAME=me@email.com" \
-e "PASSWORD=secret" \
-e "CLUB_ID=abcd1234" \
-e "TRAINING_NAME=BOXE ANGLAISE" \
clubconnect-autobooking
```

Add the script to the crontab
```
0 21 * * 1,4 /home/centos/club-connect-autobooking/clubconnect_auto_booking.sh >> /var/log/clubconnect_auto_booking.log 2>&1
```
