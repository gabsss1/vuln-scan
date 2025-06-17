import re
from models.graphcodebert import GraphCodeBERTVulnDetector

class VulnerabilityPredictor:
    def __init__(self):
        self.detector = GraphCodeBERTVulnDetector("checkpoints/")  # o usa base preentrenado

    def extract_functions(self, code: str):
        # Regex básico para detectar funciones estilo C
        pattern = r"(?:void|int|char|float|double)\s+(\w+)\s*\([^)]*\)\s*\{[^}]*\}"
        return list(re.finditer(pattern, code, re.DOTALL))

    def analyze_file(self, filepath: str):
        with open(filepath, 'r') as f:
            lines = f.readlines()
            code = ''.join(lines)

        results = []
        functions = self.extract_functions(code)

        for match in functions:
            func_code = match.group(0)
            start_line = code[:match.start()].count('\n') + 1
            func_name = re.findall(r"\b(\w+)\s*\(", func_code)[0]

            label, confidence = self.detector.predict(func_code)

            vuln_lines = []
            if label == "Vulnerable":
                for i, line in enumerate(func_code.split('\n')):
                    if any(p in line for p in ['gets(', 'strcpy(', 'scanf(', 'eval(', 'exec(', 'mysql_query']):
                        vuln_lines.append((start_line + i, line.strip()))

            results.append({
                "func_name": func_name,
                "label": label,
                "confidence": confidence,
                "vuln_lines": vuln_lines
            })

        return results