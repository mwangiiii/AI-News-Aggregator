from transformers import pipeline


# === CLASSIFICATION ===
# Load a pre-trained text classification model
classifier = pipeline('zero-shot-classification', model="facebook/bart-large-mnli")

CATEGORIES = ["Technology", "Sports", "Politics", "Business", "Health", "Entertainment"]

def categorize_article(article):
    """Classifies a news article into defined categories"""
    result = classifier(article, CATEGORIES)
    return result['labels'][0] # Return the top predicted category

# === SUMMARIZATION ===
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_article(article):
    """Summarizes a news article using a pre-trained transformer model"""
    summary = summarizer(article, max_length=10, min_length=3, do_sample=False)
    return summary[0]['summary_text']


# === Sentiment Analysis ===
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
def analyze_sentiment(article):
     """Analyzes the sentiment of a news article."""
     result = sentiment_analyzer(article)
     return result[0]['label']

if __name__ == "__main__":
    example_text = "Apple just announced the new iPhone with AI-powered features."
    print("Category:", analyze_sentiment(example_text))
