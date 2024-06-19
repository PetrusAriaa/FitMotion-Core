import asyncio
from time import time_ns
import time
from fastapi import Depends, File, UploadFile, HTTPException, APIRouter, BackgroundTasks
from google.cloud import storage
from google.auth import exceptions as google_exceptions
from os import getenv
import httpx

from .auth_router import validate_token

client = storage.Client()
bucket_name = getenv("CLOUD_BUCKET")
bucket = client.bucket(bucket_name)
storage_router = APIRouter(tags=["Storage"])

async def processing(filename, file_data):# -> dict[str, Any] | None:
    try:
        blob = bucket.blob(filename)
        blob.upload_from_string(file_data, content_type="text/csv")
    except google_exceptions.GoogleAuthError as e:
        print(e)
    except Exception as e:
        print(e)
    
    async with httpx.AsyncClient() as client:
        try:
            await client.get(f"https://fitmotion-predict-service-qoladrxgiq-et.a.run.app/predict-csv/{filename}")
        except Exception as e:
            print(e)

@storage_router.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...), session=Depends(validate_token)): 
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only .csv files are allowed.")
    id = session['id']
    filename = f'{id}-{int(time_ns()/1000)}.csv'
    
    file_data = await file.read()
    asyncio.gather(processing(filename, file_data))
    return {"status": "sent"}
