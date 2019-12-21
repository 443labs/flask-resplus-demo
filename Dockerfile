FROM ubuntu:17.10

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y python3 python-dev python3-pip python-virtualenv libpq-dev
RUN update-alternatives --remove python /usr/bin/python2.7

# Setup flask application
RUN mkdir -p /opt/flask-restplus-demo
COPY . /opt/flask-restplus-demo
RUN pip3 install -r /opt/flask-restplus-demo/requirements.txt
RUN pip3 install --no-cache-dir --ignore-installed --no-binary :all: psycopg2
ENV PYTHONPATH /opt/flask-restplus-demo/src
ENV CONFIG_DIR /opt/flask-restplus-demo/config
ENV CONFIG_ENV development
WORKDIR /opt/flask-restplus-demo

EXPOSE 5000

RUN chmod +x /opt/flask-restplus-demo/run.sh
CMD ["/opt/flask-restplus-demo/run.sh"]