FROM ubuntu:latest

RUN apt update && apt install -y python3 python3-pip
WORKDIR /usr/src/app
COPY . .
RUN python3 -m pip install -r requirements.txt
WORKDIR /usr/src/app/shopyo
RUN python3 manage.py initialise
EXPOSE 5000
CMD python3 manage.py rundebug
