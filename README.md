# twitter-clone

Simple twitter clone application, base on REST API.

## DESCRIPTION

Simple Twitter clone application with users, tweets, comments, likes, followers management system based on crude operations (create,
read, update, delete).This is application building with Python and Flask framework.
Data Management with Python, SQLite, and SQLAlchemy.

Features:

REGISTER user (post);
LOGIN user (post) + JTW;
DELETE single user (delete);
GET All users - admin only;
GET single user;
CHANGE user data for login user;
CHANGE user role - admin only;
ADD tweet (post) for login user;
GET all tweets with comments and likes counted - admin only;
GET all tweets with comments and likes counted for single user;
GET single tweet with comments and likes counted and comments with likes counted;
DELETE single tweet - admin and login user only;
ADD comment to single tweet (post) - for login user;
GET all single tweet comments with likes counted;
GET single comment with likes counted;
DELETE single comment;
GET tweet likes;
GET comment likes;
ADD tweet like (post) - for login user;
ADD comment like (post) - for login user;
FOLLOW user (post) - for login user;
GET user followers;
GET user following;
DELETE follow - for login user;
GET tweets with comments and likes counted from follow users;

## How to Set Up Project

create virtual env

`python -m venv .venv`

activate virtual env

```
# windows (cmd)
.\.venv\Scripts\activate.bat

# windows (PowerShell)
.\.venv\Scripts\activate.ps1

# macos, linux
source .venv/bin/activate
```

install project dependencies

`pip install .`

## How to run server

you can start flask application by several different way:

run as python script

`python src/01_flask_simple/app.py`

run with flask

`python -m flask --app src/app/app.py run --host 0.0.0.0 --port 8080`

run with flask (with debug & autoreload)

`python -m flask --app src/app/app.py --debug run --host 0.0.0.0 --port 8080`
