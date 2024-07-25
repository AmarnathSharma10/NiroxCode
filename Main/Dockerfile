FROM python:3.11.1

RUN apt-get update && \
    apt-get install -y gcc g++ openjdk-17-jdk

WORKDIR /niroxcode

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=Main.settings
ENV PYTHONUNBUFFERED=1

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]