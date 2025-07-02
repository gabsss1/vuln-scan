from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from predictor import VulnerabilityPredictor

app = FastAPI(
    title="Vulnerability Scanner API",
    description="Detecta vulnerabilidades en funciones de código (C/JS) usando GraphCodeBERT.",
    version="1.0.0"
)

predictor = VulnerabilityPredictor()

class CodeInput(BaseModel):
    code: str

@app.post("/scan")
def scan_code(input_data: CodeInput):
    code = input_data.code
    results = predictor.analyze_code(code)
    return {"resultados": results}

@app.post("/escanear-archivo")
async def scan_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".c") and not file.filename.endswith(".js"):
        return {"error": "Solo se permiten archivos .c o .js"}

    contents = await file.read()
    code = contents.decode("utf-8")
    results = predictor.analyze_code(code)

    return {
        "archivo": file.filename,
        "funciones_analizadas": results
    }