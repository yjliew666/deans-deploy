# Dean's Crisis Management System


# Setup envirment

## On *nix

1. Install `docker` and `docker-compose` correctly.

[How to install on mac](http://sourabhbajaj.com/mac-setup/Docker/)

2. Setup python
```shell
$ virtualenv -p python3 env 
$ source env/bin/activate
$ pip install -r requirments.txt
```

## On Windows
```
```

# Run server

If on Mac or Windows the container will run on Docker Machine which is a virtual machine, and will have its own ip address. You could run`docker-machine ip` to check the address, and such address will used to access the front end. However, on Linux, you could simplly access `localhost`.

## On *nux

If using you will need `sudo` to run the following command.
```shell
$ docker-compose up
```

## On Windows

```

```


# Useful commands

## Django migrattion

``` shell
docker-compose run web python manage.py migrate
```

# TODO

- [ ] persist data in a dockerized postgres database using volumes
- [ ] django-restful doc
- [ ] remove 'ADD' on setting page
- [ ] 
