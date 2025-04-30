# Visitor Management System Backend App
A Face-Recognition appVisitor Management System Backend application for checkin and checkouts

## Python Version
Python 3.10.11

## Create Virtual Environment
use command: `py -m venv face-env`
Then activate env:
`cd face-env/Scripts`
`./activate`
`cd ../..`

## libraries to be installed

The command to install libraries: `pip install <library-name>`
Example: `pip install fastapi pytesseract` (You can use multiple library names at once)
1. fastapi
2. pytesseract
3. mumpy
4. io
5. os
6. uuid
7. dlib
8. face_recognition
9. pil
10. openpyxl
11. pandas


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
