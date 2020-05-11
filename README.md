# Full stack Casting Agency Specifications API Backend

## About
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. 
The app is used to store Actors to casting and store Movies too.

The casting agency has a Casting Director who can post or delete actor and has a premission to modify actors or movies.
Also there is a Executive Producer who has all permissions to post or delete actors or movies and modify too
Then there is a Casting Assistant who only can view actors and movies.

The endpoints and how to send requests to these endpoints for products and items are described in the 'Endpoint Library' section of the README.

All endpoints need to be tested using curl or postman since there is no frontend for the app yet.

## Getting Started

### Installing Dependencies 

### Python 3.7
Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### PIP Dependencies

In the udacity-capstone directory, run the following to install all necessary dependencies:

```bash
pip install -r requirements.txt
```

This will install all of the required packages.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Running the server

To run the server, execute:
```
python3 app.py
or 
FLASK_APP=app.py flask run
```
We can now also open the application via Heroku using the URL:
https://capstone-karim2.herokuapp.com/

The live application can only be used to generate tokens via Auth0, the endpoints have to be tested using curl or Postman 
using the token since I did not build a frontend for the application.

## DATA MODELING:
#### models.py
The schema for the database and helper methods to simplify API behavior are in models.py:
- There are two tables created: Actors and Movies
- The Actor table is used by the roles 'Casting Director' and 'Executive Producer' to add new actor or modify actor and role 'Casting Assistant' to view data of actors and movies only
- The Movie table is used by the role 'Executive Producer' to add new movies and role 'Casting Director' to modify movies and role 'Casting Assistant' to view data of actors and movies only

Each table has an insert, update, delete, and format helper functions.

## API ARCHITECTURE AND TESTING
### Endpoint Library

@app.errorhandler decorators were used to format error responses as JSON objects. Custom @requires_auth decorator were used for Authorization based
on roles of 'Executive Producer','Casting Director' and 'Casting Assistant'

A token needs to be passed to each endpoint. 
The following works for all endpoints:
The token can be retrived by following these steps:
1. Go to https: https://kenino.auth0.com/authorize?audience=capstone&response_type=token&client_id=22m6yuDsmyruIAxdr7wWWNEUAQafknyV&redirect_uri=https://127.0.0.1:8080/login-results
2. Click on Login and enter this mail and password that used to get all permisions as 'Executive Producer':
	Email: karimemad167@gmail.com
	Password: 123456789Aa!
3. If you want to try Casting Director roles login is by using:
	Email: kimonino167@gmail.com
	Password: 123456789Aa!



#### GET '/actors'
Returns a list of all available actors , total number of actors and a success value.
By using postman:
{
    "actors": [
        {
            "age": 45,
            "gender": "female",
            "id": 1,
            "name": "Adele"
        },
        {
            "age": 23,
            "gender": "male",
            "id": 2,
            "name": "Mohamed Amin"
        },
        {
            "age": 23,
            "gender": "male",
            "id": 3,
            "name": "Mohamed ahmed"
        }
    ],
    "success": true,
    "total_actors": 3
}

#### GET '/movies'
Returns a list of all available movies, total number of movies and a success value.
By using postman:
{
    "movies": [
        {
            "id": 1,
            "release_date": null,
            "title": "Avengers"
        }
    ],
    "success": true,
    "total_movies": 1
}

#### POST '/actors'
Returns total number of actors and a success value.
By using psotman:
you should using body like it:
{
	"name":"Adele",
	"age":45,
	"gender":"female"
}
It returns:
{
    "created": 4,
    "success": true
}

#### POST '/movies'
Returns total number of movies and a success value.
By using psotman:
you should using body like it or you can don't add release_date and it will create by defult the current time you post the movie:
{
	"title":"X-Men4",
	"release_date": "Mon, 8 May 2020 10:33:30 GMT"

}
It returns:
{
    "created": 4,
    "success": true
}

#### PATCH '/actors/{actor_id}'
Returns a list of all available actors and a success value.
and if the actor id not found it return Error 404.
it's body should be:
{
	"name":"Karim",
	"age":23,
	"gender":"male"
}
it returns the list of actors and the actor you editied 
{
    "actors": [
        
        {
            "age": 45,
            "gender": "female",
            "id": 4,
            "name": "Adele"
        },
        {
            "age": 23,
            "gender": "male",
            "id": 5,
            "name": "Karim"
        }
    ],
    "success": true
}

#### PATCH '/movies/{moive_id}'
Returns a movie  and a success value.
and if the movie id not found it return Error 404.
it's body should be:
{	
	"title":"Avengers10"
}
it returns the movie you editied 
{
    "movie": [
        {
            "id": 3,
            "release_date": null,
            "title": "Snow White"
        }
    ],
    "success": true
}

#### DELETE '/actors/{actor_id}'
Return the actor id deleted, message that tell you the actor is deleted, success value and total number of actors after delete this actor 
It's return:
{
    "delete": 1,
    "message": "this actor id deleted",
    "success": true,
    "total_actors": 4
}

#### DELETE '/movies/{movie_id}'
Return the movie id deleted, message that tell you the movie is deleted, success value and total number of movies after delete this movie 
It's return:
{
    "delete": 3,
    "message": "this movie id deleted",
    "success": true,
    "total_movies": 2
}

## Testing
There are 20 unittests in test_app.py. To run this file use:
```
python test_app.py
```
The tests include one test for expected success and error behavior for each endpoint, and tests demonstrating role-based access control, 
where all endpoints are tested with and without the correct authorization.
Further, the file 'Capstone.postman_collection.json' contains postman tests containing tokens for specific roles.
To run this file, follow the steps:
1. Go to postman application.
2. Load the collection --> Import -> directory/Capstone.postman_collection.json
3. Click on the runner, select the collection and run all the tests.


## THIRD-PARTY AUTHENTICATION
#### auth.py
Auth0 is set up and running. The following configurations are in a .env file which is exported by the app:
- The Auth0 Domain Name
- The Auth0 Client ID
The JWT token contains the permissions for the 'Executive Producer' roles.

## DEPLOYMENT
The app is hosted live on heroku at the URL: 
https://capstone-karim2.herokuapp.com/

However, there is no frontend for this app yet, and it can only be presently used to authenticate using Auth0 by entering
credentials and retrieving a fresh token to use with curl or postman.