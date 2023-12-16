FROM python:latest

WORKDIR /

ENV PYTHONPATH /

COPY /. /

RUN  python3 -m pip install --upgrade pip

RUN pip freeze > requirements.txt

RUN pip3 install -r requirements.txt

CMD [ "python3", "/main.py" ]
