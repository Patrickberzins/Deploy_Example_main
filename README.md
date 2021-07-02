# Deploy_Example

Heroku provides a [good tutorial](https://devcenter.heroku.com/articles/getting-started-with-python#set-up) about how to deploy python applications in their cloud. 

This document presents a summary of the steps.

## Make sure you have an account at Heroku

Go to https://www.heroku.com and signup if you don't have an account yet.

## Installing Heroku CLI

On your mac:

```bash
brew install heroku/brew/heroku
```


## Clonning the GitHub repository for this App

Clone this repository:

```bash
git clone https://github.com/CSCI3356-Spring2021/Deploy_Example
cd ./Deploy_Example
```

**WARNING:** From now on, all commands bellow must be run from inside `Deploy_Example`.

## Creating an application

Now, change to the `Deploy_Example` folder and create a new app on your heroku by running the following command on your terminal:

```bash
heroku apps:create
```

This action must be done from inside the app source folder so that Heroku can link your source repository to your app.

## Specifying the needed runtime

Make sure you have a file called `runtime.txt` which tells Heroku the version of Python that you need. Here is the example for this application:

```
python-3.9.4
```

## Creating a requirements.txt file

You need to create a file called `requirements.txt` that tells Heroku what libraries must be installed. 
If you used a virtual environment, this command will only add the libraries/modules that were used in your apps. If you didn't use the virtual environment, the command will generate a file with all the libraries/modules installed in your computer (this may generate issues if somebody has imcompatible modules installed).

To do that:

```bash
pip freeze > ./requirements.txt
```

## Creating a Procfile

As you know, the first time you run your application, you use `python manage.py migrate` to create the models in your SQLite database (just once or every time you change your models) and then, you start your application with `python manage.py runserver` which starts a development web server at port 8080 that watches your changes to your local files as you develop and deploys these changes automatically for you.

You should never use `python manage.py runserver` to deploy an application in production. There are production web servers such as Nginx and gunicorn for that. But to keep things simple and to count on helpful hints, we will deploy in Heroku using `runserver`. `runserver` will always try to help and tell us what is wrong. A production server will not because this will often mean revealing details about your application that you don't want to reveal to an attacker. But we are learning and happy with the `runserver` can provide us.

In order to use `runserver`, create a file named `Procfile` (no extension!) with the following:

```txt
release: python manage.py migrate
web: python3 manage.py runserver 0.0.0.0:$PORT
```

Please notice that we are telling `runserver` to listen on port $PORT instead of 8080. We are doing this because Heroku dynamically assigns a port for us. When you call your application, it uses your URL to define which port to route the request to.

## Change your ALLOWED_HOSTS

When you create an Heroku application with the command `heroku apps:create`, it will assign your application a FQDN (fully qualified domain name) that starts with a random prefix such as `blooming-mesa-17823` and ends with `herokuapp.com`. So your full URL will be `https://blooming-mesa-17823.herokuapp.com` (this is just an example).

The problem is that `runserver` will not accept requests that are not comming with the host it recognizes. In order to tell `runserver` which is the random FQDN assigned to your newly created application, open the file `./config/settings.py' and change your ALLOWED_HOSTS to the following:

```
ALLOWED_HOSTS = ['localhost','127.0.0.1','.herokuapp.com',]
```

This will tell runserver that it is ok to receive requestes through URLs that end with `herokuapp.com`.

## Commit your changes

Use git to commit your changes:

```bash
git add .
git commit -m "Preparing my app for Heroku."
git push
```

## Push your main branch to the heroku origin

The previous command created a new origin in your local clone of the repository called `heroku`. Everything you push to that new origin is automatically deployed in the heroku cloud for you.

Let's now push the source and get the application deployed:

```bash
git push heroku main
```

After this command, you will see a lot of output like this:

```bash
Enumerating objects: 490, done.
Counting objects: 100% (490/490), done.
Delta compression using up to 12 threads
Compressing objects: 100% (217/217), done.
Writing objects: 100% (490/490), 86.40 KiB | 86.40 MiB/s, done.
Total 490 (delta 242), reused 490 (delta 242), pack-reused 0
remote: Compressing source files... done.
remote: Building source:
remote:
remote: -----> Building on the Heroku-20 stack
remote: -----> Determining which buildpack to use for this app
remote: -----> Python app detected
remote: -----> Installing python-3.9.4

...

remote: -----> Launching...
remote:        Released v5
remote:        https://lit-cliffs-36797.herokuapp.com/ deployed to Heroku
remote:
remote: Verifying deploy... done.
To https://git.heroku.com/lit-cliffs-36797.git

```

Wait until heroku gives you the URL for your deployed application like the example above.

## Scale the App to 1 Web Server

Make sure you have at least one web server serving your app by running the following command:

```bash
heroku ps:scale web=1
```

## Visit your App

You can now open your app with the URL you got before. If you did not save the URL, use the following command:

```bash
heroku open
```

## Remove your application from your Heroku account

```bash
heroku apps:destroy
```

