FROM python:3.8-alpine

RUN pip install flask==1.1.2 gunicorn==20.0.4

WORKDIR /app

CMD [ "gunicorn", "-b", "0.0.0.0", "app:app" ]

COPY ./ /app
