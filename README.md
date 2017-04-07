# Restaurants Web App

## About
This project provides a restaurants database interface to create, read, update, and delete restaurants and the menus for these restaurants.

## To Run
- This project requires the database to be set up.  To do this, run `python database_setup.py` in the project folder.

- This project also requires some external libraries.  If you are using vagrant to host this webserver and database, run `vagrant up` in the project folder, and `vagrant ssh` once that completes to connect to the virtual machine.  If you are not using vagrant, run the following commands:
```
$ apt-get -qqy update
$ apt-get -qqy install postgresql python-psycopg2
$ apt-get -qqy install python-flask python-sqlalchemy
$ apt-get -qqy install python-pip
$ pip install flask-httpauth
```

Now you can start the webserver by running `python restaurants_server.py`


## Future Additions
* There is a lot of repeated code in the templates that could be abstracted, like a header area that appears on every page.
