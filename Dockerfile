FROM python:3.9-slim-buster

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install make python3-dev libzmq3 

RUN pip install --no-cache -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]