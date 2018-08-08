FROM python:2-alpine
RUN mkdir /demo
COPY sendmessage.py /demo/
RUN pip install pybabblesdk
ENTRYPOINT ["python", "/demo/sendmessage.py"]
CMD []
