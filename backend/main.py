import os
import time
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup Gemini Client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")
client = genai.Client(api_key=GEMINI_API_KEY)


file_search_store_id = os.getenv("FILE_SEARCH_STORE_ID")

@app.post("/upload-ppt")
async def upload_ppt(file: UploadFile = File(...)):
    global file_search_store_id
    
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    try:
        store = client.file_search_stores.create(
            config={'display_name': f'Store_{file.filename}'}
        )
        file_search_store_id = store.name
        operation = client.file_search_stores.upload_to_file_search_store(
            file=file_path,
            file_search_store_name=file_search_store_id,
            config={'display_name': file.filename}
        )

        while not operation.done:
            time.sleep(2)
            operation = client.operations.get(operation)

        return {"message": "PPT uploaded and indexed successfully", "store_id": file_search_store_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@app.post("/ask")
async def ask_question(question: str = Form(...), file_search_store_id_param: str = Form(None)):
    
    target_store_id = os.getenv("FILE_SEARCH_STORE_ID")
    
    if not target_store_id:
        target_store_id = file_search_store_id_param
    
    if not target_store_id:
        raise HTTPException(status_code=400, detail="No Store ID available.")

    prompt = f"{question}\n\nIMPORTANT: At the end of your answer, explicitly mention the 'Slide Number' and 'Slide Title' where this information was found."

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", # Use Flash for speed/cost
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[
                    types.Tool(
                        file_search=types.FileSearch(
                            file_search_store_names=[target_store_id]
                        )
                    )
                ]
            )
        )

        answer = response.text
        
        citations = []
        if response.candidates[0].grounding_metadata:
            meta = response.candidates[0].grounding_metadata
            citations = meta.grounding_chunks

        return {
            "data" : response,
            "answer": answer,
            "citations": citations
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)