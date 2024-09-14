FROM python:3.11

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

# Instalar psql
RUN apt-get update && apt-get install -y postgresql-client

# Hacer ejecutable el script wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

CMD ["/app/wait-for-it.sh", "db", "python", "manage.py", "runserver", "0.0.0.0:8000"]