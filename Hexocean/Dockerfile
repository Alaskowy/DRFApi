FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /DRFApi
COPY requirements.txt /DRFApi/
RUN pip install -r requirements.txt
COPY . /DRFApi/