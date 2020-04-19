# Casting Agency Capstone Project
This project is my capstone project for the Udacity Full Stack Nanodegree. In it, we'll be leveraging several different pieces of technology to create web-hosted API with a database backend. The nature of this API has to do with movie casting. As we'll cover more down below, the API will cover pieces surrounding actors / actresses and their respective movies.

## Getting Started
The application itself is hosted on the Heroku platform. You can navigate to it at this link: [https://casting-api.herokuapp.com](https://casting-api.herokuapp.com).

If you navigate to the app in the browser, you will be greeted with a basic message noting that the app is indeed up and running. In order to actually use this app, you will need to be authenticated with my Auth0 domain. We'll cover more in another section how you as a Udacity reviewer might interact with this with some pre-generated tokens via Postman.

## Tech Stack
To give you a flavor on how this API was put together and deployed, we'll cover some of the pieces of the tech stack here:

- **Heroku**: This is the platform where this Git repository was pushed to and built from. It leverages the ```requirements.txt``` file to install the necessary Python libraries, ```Procfile``` to start up the Gunicorn web server, and ```manage.py``` to leverage Flask Migrate to build the PostGres database models.
- **Auth0**: Auth0 is the service we'll be using for proper authentication and authorization. We'll cover off more how this is specifically being used in another section.
- **Flask**: Flask and it's respective counterparts are what we are using to build this API in Python code. This particular Flask application contains several endpoints for various aspects of the casting API, and we'll cover that more in a future section.
- **Postman**: This isn't doing anything to enable the application itself, but it helps us with testing to ensure everything is working properly. (Additionally, there is a ```test_app.py``` file that was performed to verify unit testing.)

## Data Models

Before moving into how the API functions, it is good to know the data models supporting the API behind the scenes. In this project, we have two data models: **actors** and **movies**. The following subsections go into more details about the respective attributes of each of those models.

### Movies
- **id**: Auto-incrementing integer value
- **title**: String value
- **release_year**: Integer value

### Actors
- **id**: Auto-incrementing integer value
- **name**: String value
- **age**: Integer value
- **gender**: String value
- **movie_id**: Integer value that denotes foreign key relationship to ```id``` field in ```movies``` table

## Auth0 Roles, Permissions, and More

Within Auth0, we have established 3 high level roles and have associated different permissions for each role. Each role is progressive in the sense that a "higher" level role inherits all the permissions from a lower level one.

Here are the roles and permissions as defined in Auth0:
- **Casting Assistant**: This lowest level role only has basic view capabilities. Permissions include...
  - ```git:movies```
  - ```git:actors```
- **Casting Director**: As our middle tier role, this role inherits the same permissions from the Casting Assistant role as well as adds some additional permissions. These include...
  - ```post:movies```
  - ```post:actors```
  - ```patch:movies```
  - ```patch:actors```
- **Executive Producer**: Finally, our highest tier role contains all permissions from the roles already defined above as well as gains a few new permissions around deleting resources. These specific permissions are...
  - ```delete:movies```
  - ```delele:actors```

### Auth0 Account Setup
If you would like to setup your own account with my Auth0 instance, you can do so at the URL below. However, please note that this isn't much good for you unless add one of the respective roles above to your account. (I'm not sure how to do this in an automated fashion; this seems out of scope for this project.)

## API Endpoints

In the next few subsections, we'll cover how the API works and what you can expect back in the results.

### Default Path

#### GET /
Verifies that application is up and running on Heroku.

Sample response:
```
{
    "description": "App is running.",
    "success": true
}
```

### GET Endpoints

#### GET /movies
Displays all movies listed in the database.

Sample response:
```
{
    "movies": [
        {
            "id": 1,
            "release_year": 2020,
            "title": "Mystic River"
        },
        {
            "id": 2,
            "release_year": 2020,
            "title": "Boss Level"
        }
    ],
    "success": true
}
```

#### GET /actors
Displays all actors / actresses listed in the database.

Sample response:
```
{
    "actors": [
        {
            "age": 64,
            "gender": "male",
            "id": 1,
            "movie_id": 1,
            "name": "Frank Grillo"
        },
        {
            "age": 35,
            "gender": "female",
            "id": 2,
            "movie_id": 2,
            "name": "Scarlett Johansson"
        }
    ],
    "success": true
}
```

### POST Endpoints

#### POST /movies/
Creates a new movie entry in the database.

Sample response:
```
{
    "movies": [
        {
            "id": 2,
            "release_year": 2020,
            "title": "Boss Level"
        }
    ],
    "success": true
}
```

#### POST /actors/
Creates a new actor / actress entry in the database.

Sample response:
```
{
    "actors": [
        {
            "age": 64,
            "gender": "male",
            "id": 1,
            "movie_id": 1,
            "name": "Mel Gibson"
        }
    ],
    "success": true
}
```

### PATCH Endpoints

#### PATCH /movies/<movie_id>
Updates movie information given a movie_id and newly updated attribute info.

Sample response:
```
{
    "movies": [
        {
            "id": 1,
            "release_year": 2020,
            "title": "Mystic River"
        }
    ],
    "success": true
}
```

#### PATCH /actors/<actor_id>
Updates actor information given a actor_id and newly updated attribute info.

Sample response:
```
{
    "actors": [
        {
            "age": 64,
            "gender": "male",
            "id": 1,
            "movie_id": 1,
            "name": "Frank Grillo"
        }
    ],
    "success": true
}
```

### DELETE Endpoints

#### DELETE /movies/<movie_id>
Deletes a movie entry from the database given the inputted movie_id.

Sample response:
```
{
    "deleted": 1,
    "success": true
}
```

#### DELETE /actors/<actor_id>
Deletes an actor / actress entry from the database given the inputted actor_id.

Sample response:
```
{
    "deleted": 2,
    "success": true
}
```
