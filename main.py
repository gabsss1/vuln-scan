from models.graphcodebert import GraphCodeBERTVulnDetector
import sys
import re
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel

#Se levanta el modelo
detector = GraphCodeBERTVulnDetector("checkpoints")

app = FastAPI(
    title="Vulnerability Scanner API",
    description="Detecta vulnerabilidades en código fuente C usando GraphCodeBERT.",
    version="1.0.0"
)

class CodeInput(BaseModel):
    code: str

def marcar_lineas_vulnerables(code: str):
    patrones = ["gets(", "strcpy(", "scanf(", "eval(", "exec(", "mysql_query"]
    lineas = code.splitlines()
    lineas_vulnerables = []
    for i, linea in enumerate(lineas, 1):
        if any(pat in linea for pat in patrones):
            lineas_vulnerables.append({"line": i, "content": linea.strip()})
    return lineas_vulnerables

@app.post("/scan")
def scan_code(input_data: CodeInput):
    code = input_data.code
    resultado, prob = detector.predict(code)
    response = {
        "classification": resultado,
        "confidence": prob,
    }
    if resultado == "Vulnerable":
        response["Posibles lineas vulnerables"] = marcar_lineas_vulnerables(code)
    return response

@app.post("/escanear archivo")
async def scan_file(file: UploadFile =File(...)):
    #recibir archivo
    if not file.filename.endswith(".c"):
        return{"error":"solo archivos .c"}
    
    contents = await file.read()
    code = contents.decode("utf-8")
    
    resultado, prob = detector.predict(code)
    
    response = {
        "Nombre del archivo": file.filename,
        "Resultado": resultado,
        "Confiabilidad": prob,
    }
    if resultado == "Vulnerable":
        response["Lineas_Vulneables"] = marcar_lineas_vulnerables(code)
    return response