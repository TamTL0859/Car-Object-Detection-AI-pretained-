from fastapi import APIRouter, File, UploadFile, status, HTTPException
from fastapi.responses import FileResponse
from Logic.AIVideoProcessor import VideoProcessor
import traceback
import tempfile
import os

video_router = APIRouter()
video_router.prefix = "/video"
#http://127.0.0.1:8000/video/upload-video
#http://127.0.0.1:8001/index.html

#saves a tempfile for the "AIVideoProcessor" to process the video
@video_router.post("/upload-video", status_code=status.HTTP_200_OK)
async def POST(file: UploadFile = File(...)):
    try:
        video = await file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix='mp4') as temp_file:
                temp_file.write(video)
                temp_file_path = temp_file.name #tempfile
             
        video_processor = VideoProcessor(temp_file_path)
        processed_video_path = video_processor.process_video()
        
        return FileResponse(processed_video_path, media_type="video/mp4", filename="output.mp4")
    
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error processing video: {str(e)}")
   # finally:
       # os.remove(temp_file_path)
        