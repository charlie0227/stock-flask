FROM python:3.9.2-buster
RUN pip3 install -U pip setuptools
RUN mkdir /app
WORKDIR /app
COPY app/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY app /app
ENTRYPOINT ["python"]
CMD ["app.py"]
