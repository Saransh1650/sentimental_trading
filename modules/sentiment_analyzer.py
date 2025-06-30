from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

model_name = "ProsusAI/finbert"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
model.eval()

LABEL_TO_SCORE = {0: -1.0, 1: 0.0, 2: 1.0}

def analyze_sentiment(texts):
    scores = []
    for text in texts:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
            pred = torch.argmax(outputs.logits, dim=1).item()
            scores.append(LABEL_TO_SCORE[pred])
    avg_score = sum(scores) / len(scores) if scores else 0
    return round(avg_score, 3)