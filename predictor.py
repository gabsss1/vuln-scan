import re
from models.graphcodebert import GraphCodeBERTVulnDetector

class VulnerabilityPredictor:
    def __init__(self):
        self.detector = GraphCodeBERTVulnDetector()

    def extract_functions(self, code: str):
        pattern = r"(?:void|int|char|float|double)\s+(\w+)\s*\([^)]*\)\s*\{[^}]*\}"
        return list(re.finditer(pattern, code, flags=re.DOTALL))

    def analyze_file(self, filepath: str):
        with open(filepath, 'r') as f:
            lines = f.readlines()
            code = ''.join(lines)

        results = []
        functions = self.extract_functions(code)

        for match in functions:
            full_func = match.group(0)
            start_line = code[:match.start()].count('\n') + 1
            func_name = re.findall(r"\b(\w+)\s*\(", full_func)[0]

            label, confidence = self.detector.predict(full_func)

            vuln_lines = []
            if label == "Vulnerable":
                for i, line in enumerate(full_func.split('\n')):
                    if any(vuln in line for vuln in ['gets', 'strcpy', 'scanf("%s"', 'eval(', 'exec(', 'mysql_query']):
                        vuln_lines.append((start_line + i, line.strip()))

            results.append({
                "func_name": func_name,
                "label": label,
                "confidence": confidence,
                "vuln_lines": vuln_lines
            })
        
        return results