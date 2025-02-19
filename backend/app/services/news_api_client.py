import logging
import requests
from backend.app.config.database import NewsDatabase  # Import database
from backend.app.models.nlp_model import categorize_article, summarize_article, analyze_sentiment  # Import AI models

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class NewsAPIClient:
    API_KEY = "c086f5ef32fd4fe9b3830a78a0266281"  # Replace with your actual NewsAPI key
    BASE_URL = "https://newsapi.org/v2/top-headlines"

    def __init__(self):
        self.db = NewsDatabase()  # Initialize database connection

    def fetch_articles(self, sources):
        """Fetch news articles from NewsAPI and process them with AI."""
        articles = []

        for source in sources:
            logging.info(f"Fetching news from {source} using NewsAPI...")
            params = {
                "sources": source,
                "apiKey": self.API_KEY,
                "pageSize": 10,  # Limit number of articles
                "language": "en"
            }

            try:
                response = requests.get(self.BASE_URL, params=params)
                response.raise_for_status()
                data = response.json()

                if "articles" in data:
                    for item in data["articles"]:
                        article_text = item["description"] or item["title"]  # Use description if available

                        # Process the article using AI models
                        category = categorize_article(article_text)
                        summary = summarize_article(article_text)
                        sentiment = analyze_sentiment(article_text)

                        # Store processed article
                        processed_article = {
                            "title": item["title"],
                            "link": item["url"],
                            "content": summary,  # Store the summarized content
                            "source": source,
                            "category": category,
                            "sentiment": sentiment
                        }
                        articles.append(processed_article)

            except requests.exceptions.RequestException as e:
                logging.error(f"Failed to fetch news from {source}: {e}")

        # Save processed articles to the database
        if articles:
            self.db.save_articles(articles)
            logging.info(f"Saved {len(articles)} processed articles to the database.")

        return articles

# Example usage
if __name__ == "__main__":
    sources = ["bbc-news", "cnn", "al-jazeera-english"]  # Example sources

    client = NewsAPIClient()
    news_articles = client.fetch_articles(sources)

    for article in news_articles:
        print(article)
