import re
from models.graphcodebert import GraphCodeBERTVulnDetector

class VulnerabilityPredictor:
    def __init__(self):
        self.detector = GraphCodeBERTVulnDetector("checkpoints/")

    def extract_functions(self, code: str):
        # Regex para detectar funciones C o JS
        pattern = r"(function\s+\w+\s*\([^)]*\)\s*\{(?:[^{}]|\{[^{}]*\})*\}|(?:void|int|char|float|double)\s+\w+\s*\([^)]*\)\s*\{(?:[^{}]|\{[^{}]*\})*\})"
        return list(re.finditer(pattern, code, re.DOTALL))

    def analyze_code(self, code: str):
        results = []
        functions = self.extract_functions(code)

        for match in functions:
            func_code = match.group(0)
            start_line = code[:match.start()].count('\n') + 1
            func_name = re.findall(r"\b(\w+)\s*\(", func_code)[0]

            label, confidence = self.detector.predict(func_code)

            vuln_lines = []
            if label == "Vulnerable":
                # Detecta vulnerabilidades comunes en JS y C
                patterns = [
                    'gets(', 'strcpy(', 'scanf(',          # C
                    'eval(', 'document.write', 'innerHTML',  # JS
                    'new Function', 'setTimeout', 'setInterval', 'window.open',
                    'XMLHttpRequest', 'localStorage'
                ]
                for i, line in enumerate(func_code.split('\n')):
                    if any(p in line for p in patterns):
                        vuln_lines.append({
                            "line": start_line + i,
                            "content": line.strip()
                        })

            results.append({
                "func_name": func_name,
                "label": label,
                "confidence": confidence,
                "vuln_lines": vuln_lines
            })

        return results
