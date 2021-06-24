FROM python:3.10.0b2-buster

COPY ./ /holocron/

RUN python3 -m pip install -r /holocron/requirements.txt

CMD [ "python3", "/holocron/main.py" ]