from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class GraphCodeBERTVulnDetector:
    def __init__(self, model_path="checkpoints"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)

    def predict(self, code: str):
        inputs = self.tokenizer(code, return_tensors="pt", truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        pred = torch.argmax(probs, dim=1).item()
        return ("Segura", "Vulnerable")[pred], probs[0].tolist()