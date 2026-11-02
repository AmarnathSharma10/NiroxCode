FROM python:3.11-bookworm

RUN apt-get update && \
    apt-get install -y gcc g++ openjdk-17-jdk

WORKDIR /niroxcode

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=Main.settings
ENV PYTHONUNBUFFERED=1

CMD ["sh", "-c", "python manage.py migrate --noinput && exec gunicorn Main.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120"]