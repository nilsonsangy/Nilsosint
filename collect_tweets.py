# Import libraries
import pandas as pd
import re
import spacy
import matplotlib.pyplot as plt
import networkx as nx
from transformers import pipeline
from bertopic import BERTopic
import tweepy
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# Step 1: Collect tweets using Tweepy

def collect_tweets(keyword, limit=100):
    client = tweepy.Client(bearer_token=BEARER_TOKEN)
    tweets = []
    query = f'{keyword} -is:retweet lang:en'
    for tweet in tweepy.Paginator(client.search_recent_tweets,
                                  query=query,
                                  tweet_fields=['id', 'text', 'author_id', 'created_at'],
                                  expansions=['author_id'],
                                  max_results=100).flatten(limit=limit):
        tweets.append({
            'id': tweet.id,
            'username': tweet.author_id,  # Will resolve to username later if needed
            'tweet': tweet.text,
            'date': tweet.created_at
        })
    return pd.DataFrame(tweets)

# Fetch tweets related to DDoS
df = collect_tweets("DDoS", limit=200)

# Step 2: Sentiment analysis using a transformer model
sentiment_model = pipeline("sentiment-analysis")

# Truncate text to fit model input size
df["sentiment"] = df["tweet"].apply(lambda x: sentiment_model(x[:512])[0]['label'])

# Step 3: Topic modeling using BERTopic
topic_model = BERTopic()
topics, _ = topic_model.fit_transform(df["tweet"].tolist())
df["topic"] = topics

# Optional: visualize topics (in notebook environment)
# topic_model.visualize_topics()

# Step 4: Named Entity Recognition (NER) with spaCy
nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    doc = nlp(text)
    return [ent.text for ent in doc.ents if ent.label_ in ("PERSON", "ORG", "GPE")]

df["entities"] = df["tweet"].apply(extract_entities)

# Step 5: Build mention network from tweets
def extract_mentions(text):
    return re.findall(r'@(\w+)', text)

G = nx.DiGraph()

for _, row in df.iterrows():
    author = row["username"]
    for mentioned_user in extract_mentions(row["tweet"]):
        G.add_edge(author, mentioned_user)

# Step 6: Visualize the mention network graph
plt.figure(figsize=(12, 8))
nx.draw(G, with_labels=True, node_size=50, font_size=8, edge_color='gray')
plt.title("User Mention Network on DDoS Tweets")
plt.show()

# Optional: Show sample data
print(df[['username', 'tweet', 'sentiment', 'topic', 'entities']].head(10))

def analyze_tweets(keyword, limit=200):
    print(f"\n[1/6] Collecting tweets for '{keyword}'...")
    df = collect_tweets(keyword, limit=limit)

    print("[2/6] Running sentiment analysis...")
    sentiment_model = pipeline("sentiment-analysis")
    df["sentiment"] = df["tweet"].apply(lambda x: sentiment_model(x[:512])[0]['label'])

    print("[3/6] Running topic modeling...")
    topic_model = BERTopic()
    topics, _ = topic_model.fit_transform(df["tweet"].tolist())
    df["topic"] = topics

    print("[4/6] Running named entity recognition...")
    nlp = spacy.load("en_core_web_sm")
    def extract_entities(text):
        doc = nlp(text)
        return [ent.text for ent in doc.ents if ent.label_ in ("PERSON", "ORG", "GPE")]
    df["entities"] = df["tweet"].apply(extract_entities)

    print("[5/6] Building mention network...")
    def extract_mentions(text):
        return re.findall(r'@(\w+)', text)
    G = nx.DiGraph()
    for _, row in df.iterrows():
        author = row["username"]
        for mentioned_user in extract_mentions(row["tweet"]):
            G.add_edge(author, mentioned_user)

    print("[6/6] Visualizing mention network...")
    plt.figure(figsize=(12, 8))
    nx.draw(G, with_labels=True, node_size=50, font_size=8, edge_color='gray')
    plt.title(f"User Mention Network on '{keyword}' Tweets")
    plt.show()

    print("\nSample data:")
    print(df[['username', 'tweet', 'sentiment', 'topic', 'entities']].head(10))
    return df, G

# Example usage:
if __name__ == "__main__":
    print("\n==== Twitter Search & Analysis ====")
    print("This tool collects tweets and analyzes sentiment, topics, entities, and user mentions.")
    print("Enter a keyword or phrase to search (e.g., DDoS, ransomware, cybersecurity):")
    search_term = input("Search term: ")
    print(f"\nCollecting and analyzing tweets for: '{search_term}'\nPlease wait...")
    analyze_tweets(search_term, limit=200)
