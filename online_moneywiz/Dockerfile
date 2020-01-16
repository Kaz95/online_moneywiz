FROM python:3.6-alpine

RUN adduser -D wiz

WORKDIR /home/wiz

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY . online_moneywiz

COPY wsgi.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP wsgi.py

RUN chown -R wiz:wiz ./
USER wiz

EXPOSE 8000
ENTRYPOINT ["./boot.sh"]