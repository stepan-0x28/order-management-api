FROM python:3.11-alpine3.18

WORKDIR /usr/src

ENV PYTHONPATH=/usr/src

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

CMD [ "python", "./app/main.py" ]