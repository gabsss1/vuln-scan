from predictor import VulnerabilityPredictor
import sys

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py ruta/al/archivo.c")
        return

    filepath = sys.argv[1]
    predictor = VulnerabilityPredictor()
    results = predictor.analyze_file(filepath)

    print(f"\n📄 Analizando archivo: {filepath}\n")

    for result in results:
        print(f"🔍 Función: {result['func_name']}()")
        print(f"{'✔️ Segura' if result['label'] == 'Segura' else '⚠️ Vulnerable'} (Confianza: {result['confidence']})")

        if result['label'] == 'Vulnerable' and result['vuln_lines']:
            for line_no, content in result['vuln_lines']:
                print(f"  → Línea {line_no}: {content}")
        print()

if __name__ == "__main__":
    main()