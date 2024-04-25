from transformers import TextClassificationPipeline, pipeline
import pickle
import os
import pathlib

class Classifications:
    def __init__(self):
        self.classifications = []

    def add(self, label: str, score:float):
        self.classifications.append({"label": label, "score": score})

    def get(self):
        return self.classifications
    
    def get_argmax(self):
        if len(self.classifications) == 0:
            return None
        return sorted(self.classifications, key=lambda x: x["score"], reverse=True)[0]["label"]
    
class BaseClassification:
    def __init__(self):
        self.pipeline = None

    def predict(self, text: str)->Classifications:
        results = self.pipeline(text)
        classifications = Classifications()
        for result in results[0]:
            classifications.add(result["label"], result["score"])
        return classifications

class SentimentAnalysis(BaseClassification):
    def __init__(self):
        model: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"
        self.pipeline = TextClassificationPipeline(model=model, top_k=None)
    
class EmotionAnalysis(BaseClassification):
    def __init__(self):
        model = "SamLowe/roberta-base-go_emotions"
        self.pipeline = pipeline(task="text-classification", model=model, top_k=None)
    
class PrayerTypeClassifier(BaseClassification):
    def __init__(self):
        model = None
        tokenizer = "roberta-base"
        filePath = pathlib.Path(__file__).parent.resolve()
        cachePath = os.path.join(filePath, '..', '..', 'cache', 'prayers', 'prayer_or_praise.pkl')
        try:
            with open(cachePath, 'rb') as file:
                model= pickle.load(file)
        except Exception as e:
            print("Error loading model for prayer type classification")
            print(e)
        
        if model is None:
            model = "roberta-base"
        self.pipeline = TextClassificationPipeline(model=model, tokenizer=tokenizer, framework="pt", top_k=None)