# Visitor Management System Backend App
A Face-Recognition appVisitor Management System Backend application for checkin and checkouts

## Python Version
Python 3.10.11

## Creating Virtual environment
run sequence of commands:
1. `py -m venv face-env`
2. `cd face-env/Scripts`
3. `./activate`
4. `cd ../..`

## Packages to be installed
1. `pip install face-recognition fastapi numpy os uuid dlib io`

## Test The app
run command `uvicorn main:app --reload`