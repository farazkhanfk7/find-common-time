# Common Time to Meet
## APIs built using Django

This project was built on Python 3.11.4 and there are two branches in this project i.e : master and docker branch

- Master branch - It uses an sqlite db, which already has tables and data in it. It is easier to run if you want to run it locally.
- Docker branch - It has `Dockerfile` and `docker-compose` file and uses postgres db as service

## Run Locally

1. `$ git checkout master`
2. Create a virtualenv : `python3 -m venv env` 
3. activate : `source env/bin/activate`
4. `$ pip install -r requirements.txt`
5. `$ python manage.py runserver`

### Run Tests
1. `$ git checkout master`
2. Create a virtualenv : `python3 -m venv env` 
3. activate : `source env/bin/activate`
4. `$ pip install -r requirements.txt`
5. `$ python manage.py runserver`
6. `$ python manage.py tests`

## Run using docker-compose
1. `$ git checkout docker`
2. `docker-compose build`
3. `docker-compose up`
4. Migrations will run automatically through entrypoint.sh file
5. To create a superuser and access the admin panel :
    * `$ docker ps -a`
    * `$ docker exec -it container_id /bin/sh
    * `$ python manage.py createsuperuser`

### Postman Collection Link
``https://www.postman.com/restless-satellite-324688/workspace/dive/collection/10978920-49f9ddb9-2c1c-4afc-9b40-16ab0211cb10?action=share&creator=10978920``

## Database and API Design

- The project uses `JWT token` for authentication
- There are two models a `CustomUser` and `UserTimingPreference`
- The UserTimingPreference model has the following fields: `day_start_time`, `day_end_time`, and `timezone`. It also has a **one-to-one relationship** with the CustomUser model. This means that each user will have a corresponding UserTimingPreference object associated with them, allowing you to store and manage their timing preferences, such as the start and end times of their day and their timezone.
- I used signals in Django to automatically generate a UserTimingPreference object the moment a new user is created. This process guarantees that each user will have their own timing preferences seamlessly configured without any manual intervention.

### APIs
I was asked to make Create, Read, Update and Delete APIs for both User and UserTimingPreference.

#### User APIs
1. `POST` SignUpAPI - It serves the purpose of Create API. It registers a user and returns JWT Tokens
2. `POST` SignInAPI - Authenticate and returns JWT Tokens for user
3. `PATCH` UpdateAPI - A user can update his name and password. ( Auth Required )
4. `GET` UserDetailAPI - Returns detail of a user
5. `DELETE` UserDeleteAPI - A user can delete himself. ( Auth Required )

#### UserTimePreference APIs

1. `PATCH` UpdateUserTimePreference API - Allows a user to update his timing preferences and timezone ( Auth Required )
2. `GET` UserTimePreferenceDetail API - You can use it to get time preferences of any user

NOTE : I was asked to create all CRUD APIs for UserTimePreference model but I have not created a Create API because it is automatically created using **Django's Signals**, similarly there is no Delete API for UserTimePreference model, because according to my database design it is necessary to have a corresponding UserTimingPreference object associated with every user, i.e One-to-One relationship 

#### Suggest Meeting Slots API

`POST` Suggest Meeting Slots API : This API takes id of users, duration_mins and count of slots as query parameters and returns top n slots which don't overlap either user's calendar busy schedule. 

Note : Different users can have different timezones, but this api provides time slots in alignment with the Django project's designated timezone, as configured in the settings.py file. This ensures a uniform and consistent reference point for time-related operations across the project.
> All these APIs have test cases