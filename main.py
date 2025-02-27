# from fastapi import FastAPI, File, UploadFile, HTTPException
# from fastapi.responses import JSONResponse
# import os
# import shutil
# from cv_json_gemini import cv_json
# import json
 
# app = FastAPI()


# @app.post("/upload/")
# async def upload_file(file: UploadFile = File(...)):
#     try:
#         filename = file.filename.lower()
#         if not filename.endswith((".pdf", ".doc", ".docx")):
#             raise HTTPException(status_code=400, detail="Only PDF and Word documents are allowed")

#         file_path = os.path.join(file.filename)
#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)
        
#         extracted_json = await cv_json(file_path)
#         print(extracted_json)

#         # if not extracted_json:
#         #     raise HTTPException(status_code=500, detail="Failed to extract data. JSON response is empty.")
        
#         # print("extracted_json:", extracted_json)
#         json_dict = json.loads(extracted_json)
#         return  json_dict
 
#     except Exception as e:
#         print(f"Error: {e}")
#         raise HTTPException(status_code=500, detail=str(e))



from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Security, Depends
from fastapi.responses import JSONResponse
from fastapi.security.api_key import APIKeyHeader
import os
import shutil
import json
import tempfile
from cv_json_gemini import cv_json
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Resume Parser API", version="1.0")

# Secure API Key Authentication
API_KEY = os.getenv("your_secure_api_key")
API_KEY_NAME = os.getenv("api_key_name")

# Define API Key Security
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)):
    """Validate API Key"""
    if not api_key or api_key != API_KEY:
        raise HTTPException(status_code=403, detail=" Invalid API Key")
    return api_key

@app.post("/upload/")
async def upload_file(
    api_key: str = Depends(verify_api_key),  # Enforce API key authentication
    file: UploadFile = File(...), 
    entity: str = Form("")
):
    try:
        # Create a temporary directory to store files
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[-1]) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_file_path = temp_file.name

        print(f"Processing File: {temp_file_path}")

        # Extract JSON from document
        extracted_json = await cv_json(temp_file_path)

        # Ensure JSON parsing is successful
        # try:
        #     json_dict = json.loads(extracted_json)
        # except json.JSONDecodeError:
        #     raise HTTPException(status_code=500, detail="Failed to parse JSON response.")

        return extracted_json

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Cleanup: Remove the temp file after processing
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


