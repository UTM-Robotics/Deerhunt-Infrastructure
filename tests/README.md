## Introduction

This directory contains all tests for the backend.

## Quickstart to run tests

Make sure your server is up and running. Fill in the required config information in a .env file,
then just run 'pytest' from within the tests folder.


### To run server:
```
$ cd server/
$ ./run
```


### Running actual tests
```
$ cd tests/
$ pytest
```

If you need some more info, add verbosity.
```
$ pytest -v
```

If you only want run tests within a single file, do:
```
$ pytest -v test_auth.py
```

### Arguements
You can pass optional arguements which will override what is in .env file. These options are all defined and conftest.py
Existing options are:
```
$ pytest --flaskaddr <address:port>
$ pytest --recvemail <email_addr>
$ pytest --passwd <email_passwd>
$ pytest --adminusername <default_admin_username>
$ pytest --adminpasswd <default_admin_password>

eg: 
$ pytest --flaskaddr 192.168.0.1:5000 --recvemail testing@gmail.com  --passwd 1234
```