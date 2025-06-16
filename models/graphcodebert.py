from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class GraphCodeBERTVulnDetector:
    def __init__(self):
        self.model_name = "microsoft/codebert-base"  # o "microsoft/graphcodebert-base"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name, num_labels=2)

    def predict(self, code: str):
        inputs = self.tokenizer(code, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        pred = torch.argmax(probs, dim=1).item()
        return ("Segura", "Vulnerable")[pred], probs[0].tolist()