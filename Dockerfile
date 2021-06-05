FROM python:3.7-buster

RUN apt-get update && apt-get install -y libshout3-dev

COPY req.txt .
COPY test_req.txt .
RUN pip install -r req.txt -r test_req.txt

WORKDIR /app
copy src/ .
# copy src/tests/testdata/testconf.env .env
# copy src/tests/testdata/mock_music.db .
