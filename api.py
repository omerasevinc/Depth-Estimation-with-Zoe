from fastapi import FastAPI, File, UploadFile
from predictor import DepthEstimationModel
import upload

import os 
import uuid

ALLOWED_EXTS = {".jpg", ".jpeg", ".png"}
TEMP_FOLDER = "input_images"
os.makedirs(TEMP_FOLDER, exist_ok=True)

app = FastAPI()
depth_estimator = DepthEstimationModel()

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        file_ext = os.path.splitext(file.filename)[1]
        if file_ext not in ALLOWED_EXTS:
            return {"error":"Uploaded file must be in JPG, JPEG or PNG."}
        
        filename_base = str(uuid.uuid4())
        filename = filename_base + file_ext
        destination_path = os.path.join(TEMP_FOLDER, filename)
        output_path = os.path.join(TEMP_FOLDER, "output" + filename_base + ".png") 
        
        with open(destination_path, "wb") as image_data: 
            image_data.write(file.file.read())
            
        
        depth_estimator.calculate_depthmap(destination_path, output_path)
        response = upload.upload_image_to_imgbb(output_path)
        
        return response
    
    except Exception as e:
        return {"error": str(e)}