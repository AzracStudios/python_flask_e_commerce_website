# E-commerce App Built With Flask

## Introduction

This is a simple e-commerce web app built with the flask framework for python. The templating is handled with the "Jinja2" framework.

The frontend is built entirely using vanilla html and css. All the backend functionality, such as form submission handling, routing and static file serving are handled by flask. 


## Micro DB

Since this had to be a project that did not use any kind of 'sql' databases, a small database system, MicroDB, was built for this app. It has the bare-minimum functionality to get a backend database up and working. It allows for:
- Creating tables
- Adding rows
- Updating existing rows
- Deleting existing rows
- Fetching rows by returning matches at specific columns

It does not support any sort of foreign key handling. The database is written to the disk with the file extension ".microdb", and the data itself is plain json.


## Flask API

The frontend (html, css, jinja) and the backend (microdb) are integerated using the Flask api for python. Flask is a minimal yet powerful api built for the python programming language. In this application, it does the following:
- Manage routes (ajax request handling)
- Handle form submissions
- Handle reading and writing, from and to the database based on the requests from the frontend

## Running the app

To run the app:
- Clone or download this github repository 
- Install requirements
- Run

`$ git clone git@github.com:AzracStudios/python_flask_e_commerce_website.git`

`$ cd python_flask_e_commerce_website`

`$ pip install -r requirements.txt`

`$ python3 main.py`

This should start the flask server, which listens at port 5000 by default. Click [here to open](http://127.0.0.1:5000/)

Note: The commands might vary slightly based on the platform.

## Conclusion

This app acted as an excelent path for learning flask, and the functioning of databases under-the-hood. 

## Resources

Flask Documentation: https://flask.palletsprojects.com/en/2.2.x/

CRUD Paradigm: https://en.wikipedia.org/wiki/Create,_read,_update_and_delete

MDN Documentation: https://developer.mozilla.org/en-US/
