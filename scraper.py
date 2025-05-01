# WhoseDomain - 2025

import requests
from bs4 import BeautifulSoup
import re
import spacy
import argparse
from urllib.parse import urlparse, urljoin
import logging
import sys
import time
import random
import cloudscraper  # New library for bypassing anti-bot protections
from fake_useragent import UserAgent  # For better User-Agent rotation
import nltk
from nltk.tag import StanfordNERTagger
from nltk.tokenize import sent_tokenize, word_tokenize
nltk.download('punkt_tab')
st = StanfordNERTagger('stanford-ner/english.all.3class.distsim.crf.ser.gz', 'stanford-ner/stanford-ner.jar')

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_nlp_model():
    """Load the spaCy NLP model for named entity recognition."""
    try:
        nlp = spacy.load("en_core_web_sm")
        logger.info("Successfully loaded the spaCy NLP model")
        return nlp
    except OSError:
        logger.error("Spacy model not found. Please install it using: python -m spacy download en_core_web_sm")
        raise

def normalize_url(url):
    """Normalize a URL by adding scheme if missing."""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url

def extract_domain(url):
    """Extract the domain from a URL."""
    parsed_url = urlparse(url)
    return parsed_url.netloc

def get_random_user_agent():
    """Get a random user agent using fake_useragent library."""
    try:
        ua = UserAgent()
        return ua.random
    except:
        # Fallback to predefined list if fake_useragent fails
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/100.0.4896.85 Mobile/15E148 Safari/604.1'
        ]
        return random.choice(user_agents)

def fetch_page_content(url, retry_count=5, use_cloudscraper=True):
    """Fetch HTML content with improved anti-blocking measures."""
    for attempt in range(retry_count):
        try:
            # Randomized delay between attempts
            if attempt > 0:
                sleep_time = 3 + random.random() * 7  # 3-10 seconds random delay
                logger.info(f"Sleeping for {sleep_time:.2f} seconds before retry")
                time.sleep(sleep_time)
            
            headers = {
                'User-Agent': get_random_user_agent(),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': 'https://www.google.com/',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0',
                'Pragma': 'no-cache',
            }
            
            if use_cloudscraper:
                scraper = cloudscraper.create_scraper()
                response = scraper.get(url, headers=headers, timeout=20)
            else:
                response = requests.get(url, headers=headers, timeout=20)
            
            if response.status_code == 200:
                logger.info(f"Successfully fetched content from {url}")
                return response.text
            else:
                logger.warning(f"HTTP {response.status_code} for {url}, attempt {attempt+1}/{retry_count}")
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}, attempt {attempt+1}/{retry_count}")
    
    logger.error(f"Failed to fetch {url} after all attempts")
    return None

def extract_people_names_with_stanford(text):
    """Extract people's names from text using Stanford NER."""
    if not text:
        return set()
    
    people = set()
    for sent in sent_tokenize(text):
        tokens = word_tokenize(sent)
        tags = st.tag(tokens)
        for tag in tags:
            if tag[1] == 'PERSON':
                people.add(tag[0])
    return people

def extract_people_names(text, nlp):
    """Extract people's names from text using spaCy NER and Stanford NER."""
    if not text:
        return set()
    
    doc = nlp(text)
    people = {ent.text for ent in doc.ents if ent.label_ == "PERSON"}
    stanford_people = extract_people_names_with_stanford(text)
    people.update(stanford_people)
    return people

def filter_valid_names(people_names):
    """Filter valid names from the set of detected names."""
    valid_names = set()
    for name in people_names:
        if len(name) < 5 or len(name) > 20:  # Ensure name length is between 5 and 20 characters
            continue
        if name.isupper() or name.lower() in ["home", "projects", "about", "contact", "services", "blog"]:
            continue
        if any(char.isdigit() for char in name):  # Exclude names with numbers
            continue
        if re.match(r"^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*$", name):  # Match proper names
            valid_names.add(name)
    return valid_names

def crawl_site(domain, max_pages=20):
    """Crawl a website and collect text content, people names, internal links, and external links."""
    domain = normalize_url(domain)
    visited_urls = set()
    to_visit = {domain}
    all_text = ""
    people_names = set()
    internal_links = set()
    external_links = set()
    
    nlp = load_nlp_model()
    logger.info(f"Starting crawl of {domain}")
    
    while to_visit and len(visited_urls) < max_pages:
        current_url = to_visit.pop()
        if current_url in visited_urls:
            continue
        
        logger.info(f"Processing {current_url}")
        visited_urls.add(current_url)
        html_content = fetch_page_content(current_url)
        if not html_content:
            continue
        
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text()
        all_text += text
        people_names.update(extract_people_names(text, nlp))
        
        # Extract links
        base_domain = extract_domain(domain)
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(current_url, href)
            if extract_domain(full_url) == base_domain:
                internal_links.add(full_url)
                to_visit.add(full_url)
            else:
                external_links.add(full_url)
    
    valid_names = filter_valid_names(people_names)
    return valid_names, all_text, visited_urls, internal_links, external_links

def main():
    """Main function to parse arguments and run the crawler."""
    parser = argparse.ArgumentParser(description='Extract people names from a website or text content')
    parser.add_argument('input', help='The domain to crawl (e.g., example.com)')
    args = parser.parse_args()
    
    valid_names, all_text, visited_urls, internal_links, external_links = crawl_site(args.input)
    print("\nPotential Owners Found:")
    for name in sorted(valid_names):
        print(f"- {name}")
    print("\nPages Visited:")
    for url in visited_urls:
        print(f"- {url}")
    print("\nInternal Links Found:")
    for link in internal_links:
        print(f"- {link}")
    print("\nExternal Links Found:")
    for link in external_links:
        print(f"- {link}")

if __name__ == "__main__":
    main()