from models.graphcodebert import GraphCodeBERTVulnDetector
import sys
import re

def read_file(path):
    with open(path, "r") as file:
        return file.read()

def marcar_lineas_vulnerables(code: str):
    patrones = ["gets(", "strcpy(", "scanf(", "eval(", "exec(", "mysql_query"]
    lineas = code.splitlines()
    for i, linea in enumerate(lineas, 1):
        if any(pat in linea for pat in patrones):
            print(f"⚠️ Línea {i}: {linea.strip()}")

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py ruta/al/archivo.c")
        return

    ruta = sys.argv[1]
    code = read_file(ruta)

    detector = GraphCodeBERTVulnDetector("checkpoints")
    resultado, prob = detector.predict(code)

    print(f"📄 Archivo: {ruta}")
    print(f"🔍 Clasificación: {resultado}")
    print(f"📊 Confianza: {prob}")

    if resultado == "Vulnerable":
        print("\n📌 Posibles líneas vulnerables:")
        marcar_lineas_vulnerables(code)

if __name__ == "__main__":
    main()