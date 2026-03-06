from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from textblob import TextBlob

# -------------------------------
# SENTIMENT ANALYSIS FUNCTION
# -------------------------------
def analyze_sentiment(text):
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity

        if polarity > 0.1:
            sentiment_category = "Positive"
        elif polarity < -0.1:
            sentiment_category = "Negative"
        else:
            sentiment_category = "Neutral"

        return {
            "text": text,
            "polarity": round(polarity, 4),
            "sentiment": sentiment_category
        }
    except Exception as e:
        return {"text": text, "error": str(e)}

# -------------------------------
# FASTAPI SETUP
# -------------------------------
app = FastAPI(
    title="Sentiment Prediction API",
    description="Analyzes sentiment of tweets using TextBlob",
    version="1.0.0",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

# -------------------------------
# DATA MODELS
# -------------------------------
class TweetInput(BaseModel):
    text: str
    author: Optional[str] = "Anonymous"

class SentimentResult(BaseModel):
    text: str
    author: str
    sentiment: str
    polarity: float

class BulkAnalysisResponse(BaseModel):
    total_tweets: int
    results: List[SentimentResult]
    sentiment_distribution: dict

# -------------------------------
# API ENDPOINT
# -------------------------------
@app.post("/analyze_tweets/", response_model=BulkAnalysisResponse)
def analyze_tweets(tweets_input: List[TweetInput]):
    results = []

    for tweet in tweets_input:
        sentiment_data = analyze_sentiment(tweet.text)

        result = SentimentResult(
            text=sentiment_data["text"],
            author=tweet.author,
            sentiment=sentiment_data["sentiment"],
            polarity=sentiment_data["polarity"]
        )
        results.append(result)

    sentiments = [r.sentiment for r in results]
    sentiment_distribution = {
        "Positive": sentiments.count("Positive"),
        "Negative": sentiments.count("Negative"),
        "Neutral": sentiments.count("Neutral")
    }

    return BulkAnalysisResponse(
        total_tweets=len(results),
        results=results,
        sentiment_distribution=sentiment_distribution
    )

# -------------------------------
# RUN SERVER
# -------------------------------
if __name__ == "__main__":
    import uvicorn
    print("Sneha singh - 2330120")
    print("\n" + "="*60)
    print("Sentiment Prediction API Server Started")
    print("API Docs: http://localhost:8000/docs")
    print("="*60 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)
