FROM haifischbecken/my-test-repo:proloaf-base
COPY ./setup.py ./setup.py
COPY ./requirements.txt ./
COPY ./app ./app
ENV DEPLOYED=true
RUN pip3 install -r requirements.txt
EXPOSE 8000
CMD uvicorn app.main:app --host 0.0.0.0 --debug