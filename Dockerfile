FROM python:3.9

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt
COPY . /app

RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential gcc libsndfile1 libasound2 fluidsynth

ENTRYPOINT ["python3"]
CMD ["core.py"]

