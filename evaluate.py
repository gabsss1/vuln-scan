from datasets import load_dataset
from transformers import RobertaTokenizer, RobertaForSequenceClassification
from sklearn.metrics import classification_report
import torch

model_path = "checkpoints"
tokenizer = RobertaTokenizer.from_pretrained(model_path)
model = RobertaForSequenceClassification.from_pretrained(model_path)
model.eval()

dataset = load_dataset("json", data_files={"test": "data/test.jsonl"})["test"]

labels = [example["target"] for example in dataset]

dataset = dataset.remove_columns([col for col in dataset.column_names if col not in ["func"]])

def tokenize(example):
    return tokenizer(example["func"], padding="max_length", truncation=True, max_length=512)

dataset = dataset.map(tokenize)
dataset.set_format(type="torch", columns=["input_ids", "attention_mask"])

y_pred = []
for i in range(len(dataset)):
    inputs = {key: dataset[i][key].unsqueeze(0) for key in ["input_ids", "attention_mask"]}
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        pred = torch.argmax(probs, dim=-1).item()
    y_pred.append(pred)

# 📊 Mostramos el reporte de clasificación
print("📊 Evaluación del modelo en test.jsonl:")
print(classification_report(labels, y_pred, target_names=["Segura", "Vulnerable"]))
