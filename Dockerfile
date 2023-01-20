FROM python:3.7-alpine

RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONUNBUFFERED 1
COPY . .
CMD [ "python", "main.py", "-api_id=", "-api_hash=" ]
