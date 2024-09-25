from multiprocessing import Process, Queue
import logging
import time
import requests
import os
import pandas as pd
from bs4 import BeautifulSoup
from tweepy import OAuthHandler, API, Cursor
import imaplib
import email
from email.header import decode_header
import socks
import socket

from utils.logger import get_logger
from utils.data_cleaner import clean_urls  # Assuming you have a data_cleaner module

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Twitter API credentials (replace these with your keys)
TWITTER_CONSUMER_KEY = "your_consumer_key"
TWITTER_CONSUMER_SECRET = "your_consumer_secret"
TWITTER_ACCESS_TOKEN = "your_access_token"
TWITTER_ACCESS_SECRET = "your_access_secret"

class DataCollectionAgent(Process):
    def __init__(self, input_queue: Queue, output_queue: Queue):
        super().__init__()
        self.input_queue = input_queue  # Queue for receiving messages
        self.output_queue = output_queue  # Queue for sending messages
        self.name = "DataCollectionAgent"
        self.active = True
        self.logger = get_logger(self.name)
        self.raw_dir = 'data/raw'
        self.processed_dir = 'data/processed'
        self.output_dir = 'data/output'

        # Ensure directories exist
        os.makedirs(self.raw_dir, exist_ok=True)
        os.makedirs(self.processed_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

    def run(self):
        """
        Continuously collects URLs from various sources and sends them to the FeatureExtractionAgent.
        """
        self.logger.info(f"{self.name} started.")
        while self.active:
            try:
                urls = self.collect_urls()
                if urls:
                    self.save_urls_to_file(urls, os.path.join(self.raw_dir, 'raw_urls.csv'))
                    cleaned_urls = clean_urls(urls)
                    self.save_urls_to_file(cleaned_urls, os.path.join(self.processed_dir, 'cleaned_urls.csv'))

                    # Sending cleaned URLs to other agents for further processing
                    self.output_queue.put({"sender": self.name, "urls": cleaned_urls})

                time.sleep(86400)  # Collect URLs every 24 hours
            except Exception as e:
                self.logger.error(f"Error in {self.name}: {e}")

    def collect_urls(self):
        """
        Collects URLs from various sources including OpenPhish, PhishTank, Twitter, Email, and dark web.
        """
        self.logger.info("Starting data collection...")
        urls = []

        # Collect from OpenPhish, PhishTank, Phishing Database (same as before)
        urls += self.collect_from_openphish()
        urls += self.collect_from_phishtank()
        urls += self.collect_from_phishing_database()

        # Collect from Twitter (social media)
        urls += self.collect_from_twitter()

        # Collect from emails (IMAP)
        urls += self.collect_from_emails()

        # Collect from dark web forums (through Tor)
        urls += self.collect_from_dark_web()

        self.logger.info(f"Total URLs collected: {len(urls)}")
        return urls

    def collect_from_openphish(self):
        """Collect URLs from OpenPhish."""
        urls = []
        try:
            self.logger.info("Collecting URLs from OpenPhish...")
            response = requests.get("https://openphish.com/feed.txt")
            urls += response.text.splitlines()
            self.logger.info(f"Collected {len(urls)} URLs from OpenPhish.")
        except Exception as e:
            self.logger.error(f"Error collecting from OpenPhish: {e}")
        return urls

    def collect_from_phishtank(self):
        """Collect URLs from PhishTank."""
        urls = []
        try:
            self.logger.info("Collecting URLs from PhishTank...")
            response = requests.get("http://data.phishtank.com/data/online-valid.csv")
            df = pd.read_csv(pd.compat.StringIO(response.text))
            urls += df['url'].tolist()
            self.logger.info(f"Collected {len(df)} URLs from PhishTank.")
        except Exception as e:
            self.logger.error(f"Error collecting from PhishTank: {e}")
        return urls

    def collect_from_phishing_database(self):
        """Collect URLs from Phishing Database."""
        urls = []
        try:
            self.logger.info("Collecting URLs from Phishing.Database...")
            response = requests.get("https://phishingdatabase.com/download/all.txt")
            if response.status_code == 200:
                urls += response.text.splitlines()
            else:
                self.logger.warning(f"Failed to collect from Phishing.Database. Status code: {response.status_code}")
        except Exception as e:
            self.logger.error(f"Error collecting from Phishing.Database: {e}")
        return urls

    def collect_from_twitter(self):
        """Collect URLs from Twitter using Tweepy."""
        urls = []
        try:
            self.logger.info("Collecting URLs from Twitter...")
            auth = OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
            auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
            api = API(auth)

            for tweet in Cursor(api.search_tweets, q="http", lang="en").items(100):  # Modify search criteria as needed
                for url in tweet.entities.get("urls", []):
                    urls.append(url["expanded_url"])

            self.logger.info(f"Collected {len(urls)} URLs from Twitter.")
        except Exception as e:
            self.logger.error(f"Error collecting from Twitter: {e}")
        return urls

    def collect_from_emails(self):
        """Collect URLs from emails using IMAP."""
        urls = []
        try:
            self.logger.info("Collecting URLs from email...")
            mail = imaplib.IMAP4_SSL("imap.gmail.com")  # Use your IMAP provider
            mail.login("your_email@gmail.com", "your_password")  # Replace with actual credentials
            mail.select("inbox")

            result, data = mail.search(None, "ALL")
            email_ids = data[0].split()

            for email_id in email_ids[-10:]:  # Process the last 10 emails
                result, message_data = mail.fetch(email_id, "(RFC822)")
                for response_part in message_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        if msg.is_multipart():
                            for part in msg.walk():
                                if part.get_content_type() == "text/html":
                                    body = part.get_payload(decode=True)
                                    soup = BeautifulSoup(body, 'html.parser')
                                    for a in soup.find_all('a', href=True):
                                        urls.append(a['href'])
                        else:
                            body = msg.get_payload(decode=True)
                            soup = BeautifulSoup(body, 'html.parser')
                            for a in soup.find_all('a', href=True):
                                urls.append(a['href'])

            self.logger.info(f"Collected {len(urls)} URLs from email.")
        except Exception as e:
            self.logger.error(f"Error collecting from email: {e}")
        return urls

    def collect_from_dark_web(self):
        """Collect URLs from the dark web through Tor."""
        urls = []
        try:
            self.logger.info("Collecting URLs from dark web...")
            # Set up Tor proxy
            socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)  # Tor default proxy
            socket.socket = socks.socksocket

            response = requests.get("http://exampleonion.onion")  # Replace with actual dark web site
            soup = BeautifulSoup(response.content, 'html.parser')
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and href.startswith('http'):
                    urls.append(href)

            self.logger.info(f"Collected {len(urls)} URLs from dark web.")
        except Exception as e:
            self.logger.error(f"Error collecting from dark web: {e}")
        return urls

    def save_urls_to_file(self, urls, file_path):
        """
        Saves a list of URLs to a CSV file.
        """
        try:
            df = pd.DataFrame(urls, columns=['url'])
            df.to_csv(file_path, index=False)
            self.logger.info(f"Saved {len(urls)} URLs to {file_path}")
        except Exception as e:
            self.logger.error(f"Error saving URLs
