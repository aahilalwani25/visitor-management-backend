# Visitor Management System Backend App

A Face-Recognition appVisitor Management System Backend application for checkin and checkouts

## Python Version

Python 3.10.11

## Create Virtual Environment

use command: `py -m venv face-env`
Then activate env:

1. `cd face-env/Scripts`
2. `./activate`
3. `cd ../..`

## Install dlib

use command: `pip install dlib-19.22.99-cp310-cp310-win_amd64.whl`

## libraries to be installed

The command to install libraries: `pip install <library-name>`
Example: `pip install fastapi pytesseract` (You can use multiple library names at once)

1. fastapi
2. pytesseract
3. numpy
4. uuid
5. dlib
6. face_recognition
7. openpyxl
8. uvicorn
9. paddleocr
10. torch=2.2.1

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
