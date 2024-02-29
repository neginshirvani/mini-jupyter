FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8000

RUN python manage.py migrate --no-input
RUN python manage.py collectstatic --no-input

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
