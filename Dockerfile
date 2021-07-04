# BUILD
# docker build -t clubconnect-autobooking .
# RUN
#docker run -it --rm --name discord-bot \
#-e "USERNAME=me@email.com" \
#-e "PASSWORD=secret" \
#-e "CLUB_ID=abcd1234" \
#-e "TRAINING_NAME=BOXE ANGLAISE" \
#clubconnect-autobooking


FROM python:3.8

WORKDIR /app
ADD ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app

CMD [ "python", "-u", "./autobooking.py" ]
