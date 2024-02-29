
FROM python:3.10

ENV PYTHONUNBUFFERED=1
#ENV DJANGO_SETTINGS_MODULE=workBench.settings

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --no-input

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
