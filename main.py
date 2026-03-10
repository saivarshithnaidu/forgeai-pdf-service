from fastapi import FastAPI, UploadFile, File, HttpException
from fastapi.responses import JSONResponse
import fitz # PyMuPDF
import io

app = FastAPI(title="PDF Extraction Service")

@app.post("/extract")
async def extract_pdf_text(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Read the file content
        content = await file.read()
        
        # Open the PDF using PyMuPDF
        with fitz.open(stream=content, filetype="pdf") as doc:
            full_text = ""
            for page in doc:
                full_text += page.get_text()
        
        return JSONResponse(content={"text": full_text})
        
    except Exception as e:
        print(f"Extraction Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error extracting text: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
