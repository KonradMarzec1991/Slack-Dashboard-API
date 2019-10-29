FROM python:3.7.2

RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt /code/

RUN apt-get update
RUN apt-get install -y libxml2-dev libxmlsec1-dev libxmlsec1-openssl \
    && apt-get install -y netcat
RUN pip install -r /code/requirements.txt

COPY ./run.sh /code/run.sh

COPY . /code/

RUN chmod +x /code/run.sh
CMD /code/run.sh

