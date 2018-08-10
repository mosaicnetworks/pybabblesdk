FROM python:2-alpine
RUN mkdir /demo
COPY . /demo/
RUN pip install pybabblesdk
ENTRYPOINT ["python", "/demo/run.py"]
CMD []
