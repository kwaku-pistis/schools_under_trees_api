FROM ubuntu:groovy
RUN sudo apt update
RUN sudo apt install software-properties-common
RUN sudo add-apt-repository ppa:deadsnakes/ppa
RUN sudo apt update
RUN sudo apt install python3.7.9
RUN pip install -r app/requirements.txt
RUN mkdir -p /var/www/
WORKDIR /var/www
COPY ./app .
CMD [ "uvicorn", "app.main:app" ]
EXPOSE 8000