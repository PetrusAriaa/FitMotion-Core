from fastapi import FastAPI, File, UploadFile, HTTPException, APIRouter
from google.cloud import storage
from google.auth import exceptions as google_exceptions
import os


# Set up Google Cloud Storage client
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/root/fitmotion/FitMotion-service/service-account-key.json"
client = storage.Client()
bucket_name = "fitmotion-imu-sensor"
bucket = client.bucket(bucket_name)
storage_router = APIRouter(tags=["Storage"])    

@storage_router.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)): 
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only .csv files are allowed.")

    try:
        blob = bucket.blob(file.filename)
        blob.upload_from_file(file.file, content_type="text/csv")
        return {"message": f"File {file.filename} uploaded successfully."}
    except google_exceptions.GoogleAuthError as e:
        raise HTTPException(status_code=500, detail="Authentication error with Google Cloud.") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# To run the application, use the following command in the terminal:
# uvicorn your_script_name:app --reload
