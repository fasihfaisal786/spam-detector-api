from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import re
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')


model = joblib.load('spam_model.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')

app = FastAPI()

stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    words = text.split()
    words = [w for w in words if w not in stop_words]
    return ' '.join(words)

class MessageInput(BaseModel):
    message: str
@app.post("/predict")
def predict_spam(data: MessageInput):
    cleaned = clean_text(data.message)
    vectorized = vectorizer.transform([cleaned])
    prediction = model.predict(vectorized)[0]
    probability = model.predict_proba(vectorized)[0]
    confidence = round(max(probability) * 100, 2)
    return {
        "message": data.message,
        "prediction": prediction,
        "confidence": confidence
    }