Twitter Trending Topics Scraper
Overview
A Python-based tool to scrape the top trending topics from Twitter (X) using Selenium and MongoDB. The script logs into Twitter, navigates to the trending section, and saves the top 5 trends in MongoDB.

Execution Steps
1. Install Prerequisites
Install Python 3.7+ from python.org.
Download and install ChromeDriver matching your Chrome version from chromedriver.chromium.org.
Install MongoDB from mongodb.com.
2. Install Required Python Libraries
Run the following command to install the necessary Python packages:

bash

pip install -r requirements.txt
3. Configure Credentials & Paths
Set Twitter login credentials:
python

TWITTER_USERNAME = "your_username"
TWITTER_PASSWORD = "your_password"
Set ChromeDriver path:
python

CHROMEDRIVER_PATH = r"C:\path\to\chromedriver.exe"
MongoDB URI (optional if you use a custom URI):
python

MONGO_URI = "mongodb://localhost:27017/"
4. Run the Script
Execute the script to fetch the latest trending topics:

bash

python twitter_trending.py
This will output the top 5 trending topics and store them in MongoDB.

5. Check MongoDB for Data
Ensure MongoDB is running.
The data is stored in the twitter_trends database, trends collection.
Notes
XPath changes: Twitter’s page structure may change over time, breaking the script. Update XPaths if needed.
This project fetches only the top 5 trending topics at the time of execution.
