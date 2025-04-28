from fastapi import FastAPI, File, UploadFile
import face_recognition
from fastapi.responses import JSONResponse
import numpy as np
import io
import os
import uuid

upload_user_checkin_pics_directory= "known_users_images"
upload_user_checkin_encodings_directory= "known_users_encodings"

app = FastAPI()

@app.post('/checkin/')
async def checkin_user(file: UploadFile):
    try:
        image = await file.read()
        extension= file.filename.split('.')[1]
        v4= uuid.uuid4()
        file_location_for_known_users_images= f"./{upload_user_checkin_pics_directory}/{v4}.{extension}"
        #file_location_for_known_users_encodings= f"./{upload_user_checkin_encodings_directory}/{v4}.{extension}"
        #print(encodings)
        os.makedirs(upload_user_checkin_pics_directory,exist_ok=True)
        os.makedirs(upload_user_checkin_encodings_directory, exist_ok=True)

        with open(file_location_for_known_users_images,"wb") as buffer:
            buffer.write(image)

        # Load image and extract face encodings
        img = face_recognition.load_image_file(io.BytesIO(image))
        encodings = face_recognition.face_encodings(img)

        if not encodings:
            return JSONResponse(
                status_code=400,
                content={"message": "No face found in uploaded image."}
            )

        # Save first face encoding (you can handle multiple faces if needed)
        encoding_file_path = os.path.join(upload_user_checkin_encodings_directory, f"{v4}.npy")
        np.save(encoding_file_path, encodings[0])

        return JSONResponse(
            status_code=200,
            content={
                "fileName": f"{v4}.{extension}",
                "encodingFile": f"{v4}.npy"
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
                        "message": "User recognized",
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
