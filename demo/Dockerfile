FROM python:2-alpine
RUN mkdir /demo
COPY sendmessage.py /demo/
RUN pip install pybabblesdk
ENTRYPOINT ["python", "/demo/sendmessage.py"]
CMD []

#FROM python:2-alpine
#RUN mkdir /demo && mkdir /demo/pybabblesdk
#COPY pybabblesdk /demo/pybabblesdk
#COPY sendmessage.py /demo/
#ENV PYTHONPATH=$PYTHONPATH:/demo/pybabblesdk
#RUN python -m pip install six
#ENTRYPOINT ["python", "/demo/sendmessage.py"]
#CMD []
