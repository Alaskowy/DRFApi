#Django Rest Framework Image API

##Table of contents
* [General Info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Endpoints](#endpoints)

##General Info

This is a project created to take a part in recruitment process. Work time circa 3 working days.

##Technologies

* Python 3.10
* Django
* Django REST Framework
* Redis
* Pillow
* PostgreSQL

## Setup

Prepare .env file with following:
```
SECRET_KEY=<your_secret_key>
DEBUG=True

POSTGRES_DB=drfapi
POSTGRES_USER=postgres
POSTGRES_PASSWORD=123
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_ATOMIC_REQUESTS=True

REDIS_LOCATION=redis://redis:6379
REDIS_USERNAME=''
REDIS_PASSWORD=''
```

Make sure you're in the proper directory, and run the docker-compose up command:


```
cd /Hexocean
docker-compose up
```

## Endpoints

For uploading images and fetching them use:
```
localhost:8000/api/images
```

For fetching link to binary image:

```
localhost:8000/api/images/<pk>/link?expires=<seconds>
```





