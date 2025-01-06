FROM ubuntu:22.04

RUN apt update && apt upgrade -y && apt install python3-pip python3-dev libpq-dev gcc -y

WORKDIR /app
COPY . /app
RUN pip3 install --no-cache-dir -r requirements.txt

CMD flask run