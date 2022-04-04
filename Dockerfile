FROM python:3.9-slim-buster

WORKDIR /app

COPY . .

RUN apt-get update
# && apt-get install -y make python3-dev libzmq3-dev ffmpeg libsm6 libxext6

RUN pip install --no-cache -r requirements.txt && chmod 777 ./entrypoint.sh 

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]