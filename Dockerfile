FROM python:3
COPY ./requirements.txt ./
COPY ./app ./app
RUN pip3 install -r requirements.txt
CMD uvicorn app.main:app