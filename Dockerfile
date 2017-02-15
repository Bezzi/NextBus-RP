FROM python:3
RUN pip3 install redis
RUN pip3 install requests
RUN pip3 install requests_cache
RUN pip3 install pymongo
RUN apt-get update
RUN apt-get install -y redis-server supervisor

ADD revproxy.py /
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD [ "/usr/bin/supervisord" ]
