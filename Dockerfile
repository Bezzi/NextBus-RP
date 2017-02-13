FROM python:3
ADD Run.py /
RUN pip3 install redis
RUN pip3 install requests
RUN pip3 install requests_cache
RUN pip3 install pymongo
CMD [ "python3", "./Run.py" ]
