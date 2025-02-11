import logging
import schedule
import time
from scraper import NewsScraper
from database import NewsDatabase
from duplicate_checker import DuplicateChecker
from news_api_client import NewsAPIClient

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Define news sources for web scraping
NEWS_SOURCES = [
    {"name": "Kenyans", "url": "https://www.kenyans.co.ke/", "article_selector": "h2"},
    {"name": "BBC", "url": "https://www.bbc.com/news", "article_selector": "h3"},
    {"name": "CNN", "url": "https://edition.cnn.com/world", "article_selector": "h3"}
]

# API sources
NEWS_API_SOURCES = ["bbc-news", "cnn", "al-jazeera-english"]  # Example sources

def fetch_news():
    """Main function to scrape, fetch from APIs, filter, and save news articles."""
    logging.info("Starting News Aggregator...")

    db = NewsDatabase()
    duplicate_checker = DuplicateChecker()
    all_articles = []

    # Step 1: Scrape news articles
    for source in NEWS_SOURCES:
        logging.info(f"Scraping from {source['name']}...")

        try:
            scraper = NewsScraper([source])
            articles = scraper.run()

            if articles:
                all_articles.extend(articles)
            else:
                logging.warning(f"No articles found for {source['name']}.")

        except Exception as e:
            logging.error(f"Error scraping {source['name']}: {e}")

    # Step 2: Fetch news from NewsAPI
    news_api_client = NewsAPIClient()
    api_articles = news_api_client.fetch_articles(NEWS_API_SOURCES)

    if api_articles:
        all_articles.extend(api_articles)

    logging.info(f"Total articles collected: {len(all_articles)}")

    # Step 3: Remove duplicates
    unique_articles = duplicate_checker.remove_duplicates(all_articles)
    logging.info(f"Unique articles after filtering: {len(unique_articles)}")

    # Step 4: Save to database
    if unique_articles:
        db.save_articles(unique_articles)
        logging.info("News articles successfully stored in the database.")
    else:
        logging.info("No new unique articles to store.")

    # Close DB connection
    db.close_connection()
    logging.info("Database connection closed. Aggregation complete.")

# Automated Fetching (Scheduling)
# The schedule library ensures the system runs automatically every hour.
# This means fresh news is collected without manual intervention.

# Scheduler: Run the job every hour
schedule.every(1).hour.do(fetch_news)

if __name__ == "__main__":
    fetch_news()  # Run immediately

    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute
