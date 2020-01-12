FROM python:3.6-alpine
RUN adduser -D moneywiz
WORKDIR /home/moneywiz
COPY requirements.txt  requirements.txt
#RUN python3 -m venv venv
#RUN venv/bin/pip3 install -r requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "app.py"]
#CMD ["venv/bin/python", "app.py"]