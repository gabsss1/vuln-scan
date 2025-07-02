from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class GraphCodeBERTVulnDetector:
    def __init__(self, model_path="checkpoints"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)

    def predict(self, code: str):
        tokens = self.tokenizer(code, return_tensors="pt", truncation=False, padding=False)["input_ids"][0]

        if tokens.shape[0] <= 512:
            inputs = self.tokenizer(code, return_tensors="pt", truncation=True, padding=True, max_length=512)
            with torch.no_grad():
                outputs = self.model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
            pred = torch.argmax(probs, dim=1).item()
            return ("Segura", "Vulnerable")[pred], probs[0].tolist()

        chunks = tokens.split(512)
        confidences = []
        vulnerable = False

        for chunk in chunks:
            inputs = {"input_ids": chunk.unsqueeze(0)}
            with torch.no_grad():
                outputs = self.model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
            confidences.append(probs[0])
            if torch.argmax(probs, dim=1).item() == 1:
                vulnerable = True

        avg_conf = torch.mean(torch.stack(confidences), dim=0).tolist()
        return ("Vulnerable" if vulnerable else "Segura"), avg_conf