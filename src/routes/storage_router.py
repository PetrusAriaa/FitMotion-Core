from time import time_ns
from fastapi import Depends, File, UploadFile, HTTPException, APIRouter
from google.cloud import storage
from google.auth import exceptions as google_exceptions
from os import getenv

from .auth_router import validate_token

client = storage.Client()
bucket_name = getenv("CLOUD_BUCKET")
bucket = client.bucket(bucket_name)
storage_router = APIRouter(tags=["Storage"])    


@storage_router.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...), session=Depends(validate_token)): 
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only .csv files are allowed.")

    try:
        id = session['id']
        blob = bucket.blob(f'{id}-{int(time_ns()/1000)}')
        blob.upload_from_file(file.file, content_type="text/csv")
        return {"message": f"File {file.filename} uploaded successfully."}
    except google_exceptions.GoogleAuthError as e:
        raise HTTPException(status_code=500, detail="Authentication error with Google Cloud.") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
