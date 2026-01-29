import streamlit as st
import feedparser
import pandas as pd
from datetime import datetime

# The Atlas Agentic Target List
FEEDS = {
    "STAT News": "https://www.statnews.com/feed/",
    "Fierce Biotech": "https://www.fiercebiotech.com/rss",
    "BioPharma Dive": "https://www.biopharmadive.com/feeds/news/",
    "Nature Biotech": "https://www.nature.com/nbt.rss",
    "Labiotech.eu": "https://www.labiotech.eu/feed/",
}

def fetch_biotech_intel():
    intel_data = []
    
    for source, url in FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:  # Get the top 5 latest news per source
            intel_data.append({
                "Source": source,
                "Headline": entry.title,
                "Link": entry.link,
                "Published": entry.get('published', 'N/A'),
                "Scrape_Date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            
    return pd.DataFrame(intel_data)

# Run the Scraper
df = fetch_biotech_intel()

# Filter for LMIC or Policy Gaps (Example)
keywords = ['Africa', 'Manufacturing', 'EU', 'Policy', 'mRNA', 'Transfer']
gap_signals = df[df['Headline'].str.contains('|'.join(keywords), case=False)]

print("--- LATEST BIOTECH SIGNALS ---")
print(df[['Source', 'Headline']].head(10))

print("\n--- PRIORITY TRANSLATION GAPS FOUND ---")
print(gap_signals[['Source', 'Headline']])
