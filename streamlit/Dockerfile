FROM python:3.8.0-slim

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt

RUN pip3 install -r requirements.txt

COPY . /app

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]