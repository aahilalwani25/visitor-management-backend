from fastapi import FastAPI, UploadFile, Request, Body
import face_recognition
from fastapi.responses import JSONResponse
import numpy as np
import io
from PIL import Image
import os
from fastapi.middleware.cors import CORSMiddleware
import uuid
import pytesseract
import firebase_admin
from firebase_admin import credentials
from models.user_model import User
import pandas as pd
from openpyxl import load_workbook, Workbook



upload_user_checkin_pics_directory= "known_users_images"
upload_user_checkin_encodings_directory= "known_users_encodings"
pytesseract.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Initialize Firebase Admin SDK (replace 'path/to/your/serviceAccountKey.json' with the actual path)
cred = credentials.Certificate('./face-recognition-1579d-firebase-adminsdk-fbsvc-444ef07505.json')
firebase_admin.initialize_app(cred)

# Define the file name
file_name = "visitors.xlsx"
file_path = os.path.join(os.getcwd(), file_name)



app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # or specify ['POST', 'GET', ...]
    allow_headers=["*"],  # or specify ['Authorization', 'Content-Type', ...]
)

@app.post('/checkin/')
async def checkin_user(file: UploadFile):
    try:
        image = await file.read()
        extension= file.filename.split('.')[1]
        v4= uuid.uuid4()
        file_location_for_known_users_images= f"./{upload_user_checkin_pics_directory}/{v4}.{extension}"
        # Load image and extract face encodings
        img = face_recognition.load_image_file(io.BytesIO(image))
        encodings = face_recognition.face_encodings(img)

        if not encodings:
            print("No face found in uploaded image")
            return JSONResponse(
                status_code=400,
                content={
                    "data":{
                        "message": "No face found in uploaded image."
                    }
                }
            )
        os.makedirs(upload_user_checkin_pics_directory,exist_ok=True)
        os.makedirs(upload_user_checkin_encodings_directory, exist_ok=True)

        with open(file_location_for_known_users_images,"wb") as buffer:
            buffer.write(image)

        # Save first face encoding (you can handle multiple faces if needed)
        encoding_file_path = os.path.join(upload_user_checkin_encodings_directory, f"{v4}.npy")
        np.save(encoding_file_path, encodings[0])

        return JSONResponse(
            status_code=200,
            content={
                "message":"Checked in"
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": 500,
                "message": str(e)
            }
        ) 

@app.post('/checkout/')
async def recognize_user(file: UploadFile):
    try:
        # Read uploaded image
        image = await file.read()

        # Load uploaded image and encode
        img = face_recognition.load_image_file(io.BytesIO(image))
        unknown_encodings = face_recognition.face_encodings(img)

        if not unknown_encodings:
            return JSONResponse(
                status_code=400,
                content={"message": "No face found in uploaded image."}
            )

        unknown_encoding = unknown_encodings[0]

        # Load all known encodings
        known_encodings = []
        known_ids = []

        for filename in os.listdir(upload_user_checkin_encodings_directory):
            if filename.endswith('.npy'):
                filepath = os.path.join(upload_user_checkin_encodings_directory, filename)
                encoding = np.load(filepath)
                known_encodings.append(encoding)
                user_id = filename.split('.')[0]  # uuid as user id
                known_ids.append(user_id)

        # Compare the uploaded face with all known faces
        results = face_recognition.compare_faces(known_encodings, unknown_encoding, tolerance=0.5)

        for idx, match in enumerate(results):
            if match:
                matched_user_id = known_ids[idx]
                return JSONResponse(
                    status_code=200,
                    content={
                        "message": "Checked out",
                        "user_id": matched_user_id
                    }
                )

        return JSONResponse(
            status_code=404,
            content={"message": "No matching user found."}
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": 500,
                "message": str(e)
            }
        )
    
# @app.post('/scan-cnic/')
# async def scan_cnic(file: UploadFile):
#     try:
#         # Read and convert uploaded image
#         contents = await file.read()
#         image = Image.open(io.BytesIO(contents))

        
#     except Exception as e:
#         return JSONResponse(
#             status_code=500,
#             content={
#                 "status": 500,
#                 "message": str(e)
#             }
#         )
        

@app.post('/create-user/')
async def create_user(user: User):
    try:
        # Check if the file exists
        if os.path.exists(file_path):
            workbook = load_workbook(file_path)
            sheet = workbook.active
        else:
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Sheet1"
            # Write column headers only once when creating a new file
            headers = ["full_name", "cnic", "check_in", "check_out","user_id"]
            sheet.append(headers)

        # Append user data as a new row
        new_row = [user.full_name, user.cnic, user.check_in, "", user.user_id]
        sheet.append(new_row)

        # Save the updated Excel file
        workbook.save(file_path)

        return JSONResponse(
            status_code=200,
            content={"message": "User data saved successfully"}
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": str(e)}
        )