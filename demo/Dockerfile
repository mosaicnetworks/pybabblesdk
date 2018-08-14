FROM python:2-alpine
RUN mkdir /demo
COPY . /demo/
RUN pip install six
RUN pip install requests
ENTRYPOINT ["python", "/demo/sendmessage.py"]
CMD []
