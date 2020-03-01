FROM python:3.7.6

EXPOSE 5000/tcp

ENV PYTHONPATH /lib/notes

ADD ./notes /lib/notes/notes
ADD ./requirements.txt /lib/notes

RUN pip install -r /lib/notes/requirements.txt

WORKDIR /lib/notes

CMD uwsgi --http :5000 --processes 2 --threads 2 --wsgi-file notes/app.py --callable app
