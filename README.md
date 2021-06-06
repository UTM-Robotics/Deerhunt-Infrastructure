#  Official Deerhunt Infrastructure

This is the official repo of the Deerhunt Website developed and run by UTM Robotics Club. This is an open source project maintained by our students.

This README will be update accordingly as the project moves forward.

## Folder Structure
```
.
├── deerhunt/
│   ├── package.json
│   ├── package-lock.json
│   ├── public/
│   ├── README.md
│   └── src/
├── tests/
│   ├── ref
│   └── test_auth.py
├── server/
│   ├── app.py
│   └── requirements.txt
├── install.sh
└── README.md
```
**deerhunt/**: Everything to do with the frontend lives here. You will find npm related files here as well as the frontend source files.

**server/**: All backend source files live in this folder.

**tests/**: All unittests at least for the backend will live here. Currently empty but will be populated soon. Make sure you are familiar with  [Pytest Framework](https://docs.pytest.org/en/6.2.x/#).

## Requirements
```
A unix based computer
git
python3+
npm
```
 
##  Development Setup Instructions
I encourage you to go through the install script to understand what it is doing before running it. Once it runs you should have a folder called **venv/** created and your terminal should look something like this:
```
$ (venv) adl@Cronos ~/git/deerhunt2020/infrastructure
``` 
If you need to read up on python virtual environments you can do so [here](https://docs.python.org/3/tutorial/venv.html).

**It is important that you source the install.sh instead of just running it the traditional way.**

### Ubuntu / Debian
It is important that you have a Linux installation such as Ubuntu / Debian which uses [apt](https://linux.die.net/man/8/aptitude) as its package manager since the script uses it. Also make sure you keep your system packages up to date.
```
$ sudo apt update
$ sudo apt upgrade -y
$ source ./install.sh
```

### Mac OSX
Make sure you have [Homebrew](https://brew.sh/) installed and updated before running the script below.
```
$ brew update
$ brew doctor
$ source ./install.sh
```


### Windows 
~~It is highly recommended to setup your development environment on a Linux machine. If you are on Windows and don't have access to a local Ubuntu / Debian computer, you can ssh into the UTM Deerfield CS lab which hosts Ubuntu by doing the following:~~
```
$ ssh <UTORid>@dh<XXXX>pc<YY>.utm.utoronto.ca
Where:
<UTORid> is your UofT acorn username.
<XXXX> is CS Lab number (eg: 2020 or 2026).
<YY> is the computer number in the lab.

Example:
$ ssh linalex7@dh2026pc01.utm.utoronto.ca
```

##  Production Instructions
To be complete when infrastructure is ready for production.
