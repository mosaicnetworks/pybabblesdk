FROM python:2-alpine
RUN mkdir /demo
COPY . /demo/
RUN pip install pybabblesdk --no-cache
ENTRYPOINT ["python", "/demo/run.py"]
CMD []
