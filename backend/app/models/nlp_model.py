from transformers import pipeline


# === CLASSIFICATION ===
# Load a pre-trained text classification model
classifier = pipeline('zero-shot-classification', model="facebook/bart-large-mnli")

CATEGORIES = ["Technology", "Sports", "Politics", "Business", "Health", "Entertainment"]

def categorize_article(article):
    """Classifies a news article into defined categories"""
    result = classifier(article, CATEGORIES)
    return result['labels'][0] # Return the top predicted category

# Example usage
if __name__ == "__main__":
    example_text = "Apple just announced the new iPhone with AI-powered features."
    print("Category:", categorize_article(example_text))

# === CLASSIFICATION ===

