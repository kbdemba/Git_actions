FROM python:3.6

WORKDIR /sso_example

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . ./
RUN chmod a+x boot.sh

ENV FLASK_APP=sso_example.py

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
