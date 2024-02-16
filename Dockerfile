FROM python:3.9

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./src /app/src
ENV FLASK_APP=/app/src/hotel

ENTRYPOINT ["flask", "run", "--host=0.0.0.0", "--debug"]
