# Code Vulnerability Detector

Sistema de clasificación de funciones en código como **seguras** o **vulnerables** usando modelos de lenguaje como GraphCodeBERT.

## Modelos soportados
- ✅ GraphCodeBERT (`microsoft/codebert-base`)
- 🧪 Devign (experimental)
- 🧪 VulBERTa (requiere fine-tuning)

## Cómo usar

```bash
python main.py data/ejemplo_vulnerable.c