FROM python:3.6-alpine
COPY . /app
WORKDIR /app
#COPY requirements.txt  requirements.txt
#RUN python3 -m venv venv
#RUN venv/bin/pip3 install -r requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn
EXPOSE 8000

COPY . /app

CMD ["gunicorn", "-b", "0.0.0.0:8000", "wsgi:app"]
#CMD ["python3", "routes.py"]
#CMD ["venv/bin/python", "routes.py"]