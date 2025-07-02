from datasets import load_dataset
from transformers import RobertaTokenizer, RobertaForSequenceClassification, TrainingArguments, Trainer

# Cargar dataset
data_files = {
    "train": "data/train.jsonl",
    "validation": "data/valid.jsonl"
}
dataset = load_dataset("json", data_files=data_files)
dataset = dataset.remove_columns([col for col in dataset["train"].column_names if col not in ["func", "target"]])

# Tokenización
model_name = "microsoft/graphcodebert-base"
tokenizer = RobertaTokenizer.from_pretrained(model_name)

def tokenize(example):
    return tokenizer(example["func"], padding="max_length", truncation=True, max_length=512)

dataset = dataset.map(tokenize, batched=True)
dataset = dataset.rename_column("target", "labels")

# Modelo
model = RobertaForSequenceClassification.from_pretrained(model_name, num_labels=2)

# Entrenamiento
training_args = TrainingArguments(
    output_dir="./checkpoints",
    num_train_epochs=15,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    logging_dir="./logs",
    load_best_model_at_end=True,
    logging_steps=10,
    save_total_limit=1
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["validation"],
    tokenizer=tokenizer
)

trainer.train()

# Guardar modelo
trainer.save_model("checkpoints/")
tokenizer.save_pretrained("checkpoints/")