from fastapi import FastAPI, HTTPException, UploadFile, status
from .classifier import classify

app = FastAPI()


async def __validate_file(file: UploadFile):
    if (file.content_type != 'text/csv'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid file type",
                            headers={"Content-Type": "text/csv"})
    # FIELDS = ['attitude.roll', 'attitude.pitch', 'attitude.yaw', 'gravity.x', 'gravity.y', 'gravity.z', 'rotationRate.x', 'rotationRate.y', 'rotationRate.z', 'userAcceleration.x', 'userAcceleration.y', 'userAcceleration.z']
    # data = await file.read()
    # strf = data.decode()
    # try:
    #     # stripped = strf.split('\n')[0].split(',') 
    # except Exception as e:
    #     print(e)
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
    #                         detail=f"Unprocessable file. {e}",
    #                         headers={"Content-Type": "text/csv"})
    # if strf.split('\n')[0].split(',')[1:] != FIELDS:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
    #                         detail=f"Unprocessable file. Please check your CSV header. Missing required fields in order. {FIELDS}",
    #                         headers={"Content-Type": "text/csv"})
    return await file.read()

@app.get('/health', tags=['Healthcheck'])
def ping():
    return {"message": "pong"}


@app.post('/api/detect', tags=['Motion Detect'])
async def detect_motion(file: UploadFile):
    b_file = await __validate_file(file)
    result, proc_time = await classify(b_file)
    return {"result" : result, "procTimeMS": proc_time}