# django-bot-server-tutorial

Accompanying repository for a seminar on creating a django based bot server that uses django-channels for  WebSockets connection. This borrows heavily from the code at https://github.com/andrewgodwin/channels-examples 

# What is this useful for?

- Get an idea how to get django-channels working
- Get some sample code for a simple working front end that uses web sockets for a connection

# How to use this branch

This part of the seminar involves installing and getting started with django channels.

To get this running, simply run the  the following 

## Step 1: Install requirements.txt

`pip install -r requirements.txt`

## Step 2: Create databases

Create the databases and the initial migrations with the following command:
`python manage.py migrate`

## Step 3: Run server

And start the server with 

`python manage.py runserver`

You should now be able to go to localhost:8000/chat/ and chat with the bot


## Updated changes (User and Button History added):

### Step 1
Sign up your profile to the application. This can be achieved through `localhost:8000/signup/` API.
### Step 2
After the successful signup, login with the credentials and the API route is `localhost:8000/login/`
### Step 3
You will be redirected to chat window, and it contains `FAT, STUPID, DUMB` buttons.
### Step 4
To view the users list and count of the buttons they hit, use `localhost:8000/users-list/` API.
