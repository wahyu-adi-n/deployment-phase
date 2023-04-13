FROM python:3.8.0-slim

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip3  install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install opencv-python-headless

COPY . /app

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
