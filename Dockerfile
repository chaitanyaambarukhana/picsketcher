FROM tensorflow/tensorflow

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install python3-tk -y
# && apt-get install -y make python3-dev libzmq3-dev ffmpeg libsm6 libxext6

RUN pip install --upgrade pip && pip install --no-cache -r requirements.txt && chmod 777 ./entrypoint.sh 

EXPOSE 8000
