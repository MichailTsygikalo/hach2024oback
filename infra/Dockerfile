FROM python:3.12
WORKDIR /proj
COPY ./requirements.txt requirements.txt 
RUN python3.12 -m pip install -r requirements.txt
COPY ./ ./