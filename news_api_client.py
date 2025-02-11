import logging
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class NewsAPIClient:
    API_KEY = "c086f5ef32fd4fe9b3830a78a0266281"  # Replace with your actual NewsAPI key
    BASE_URL = "https://newsapi.org/v2/top-headlines"

    def fetch_articles(self, sources):
        """Fetch news articles from NewsAPI for given sources."""
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
                        articles.append({
                            "title": item["title"],
                            "link": item["url"],
                            "content": item["description"] or "",
                            "source": source
                        })

            except requests.exceptions.RequestException as e:
                logging.error(f"Failed to fetch news from {source}: {e}")

        return articles
