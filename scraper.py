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

def get_random_referrer():
    """Get a random referrer URL to make requests look more legitimate."""
    referrers = [
        'https://www.google.com/',
        'https://www.bing.com/',
        'https://www.yahoo.com/',
        'https://duckduckgo.com/',
        'https://twitter.com/',
        'https://www.linkedin.com/',
        'https://www.facebook.com/'
    ]
    return random.choice(referrers)

def fetch_page_content(url, retry_count=5, use_cloudscraper=True):
    """Fetch HTML content with improved anti-blocking measures."""
    for attempt in range(retry_count):
        try:
            # Randomized delay between attempts (longer than before)
            if attempt > 0:
                sleep_time = 3 + random.random() * 7  # 3-10 seconds random delay
                logger.info(f"Sleeping for {sleep_time:.2f} seconds before retry")
                time.sleep(sleep_time)
            
            # Randomized request headers with more parameters
            headers = {
                'User-Agent': get_random_user_agent(),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': get_random_referrer(),
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0',
                'Pragma': 'no-cache',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'cross-site',
                'Sec-Fetch-User': '?1',
            }
            
            if use_cloudscraper:
                # Use cloudscraper to bypass Cloudflare and similar protections
                scraper = cloudscraper.create_scraper(browser={
                    'browser': 'chrome',
                    'platform': 'windows',
                    'mobile': False
                })
                response = scraper.get(
                    url, 
                    headers=headers, 
                    timeout=20,
                    allow_redirects=True
                )
            else:
                # Use regular requests as fallback
                session = requests.Session()
                response = session.get(
                    url, 
                    headers=headers, 
                    timeout=20,
                    allow_redirects=True
                )
            
            if response.status_code == 200:
                logger.info(f"Successfully fetched content from {url}")
                return response.text
            elif response.status_code == 403:
                logger.warning(f"Access forbidden (403) for {url}, attempt {attempt+1}/{retry_count}")
                # If using regular requests and getting 403, try cloudscraper next time
                if not use_cloudscraper:
                    use_cloudscraper = True
                    logger.info("Switching to cloudscraper for next attempt")
            else:
                logger.warning(f"HTTP {response.status_code} for {url}, attempt {attempt+1}/{retry_count}")
                
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}, attempt {attempt+1}/{retry_count}")
    
    # Try a different approach on the last retry
    if retry_count > 0:
        try:
            logger.info("Trying a final approach with selenium...")
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service
            from webdriver_manager.chrome import ChromeDriverManager
            
            # Set up headless Chrome
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument(f'--user-agent={get_random_user_agent()}')
            
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.get(url)
            
            # Wait for page to load
            time.sleep(5)
            
            html_content = driver.page_source
            driver.quit()
            
            if html_content:
                logger.info(f"Successfully fetched content from {url} using Selenium")
                return html_content
                
        except Exception as e:
            logger.error(f"Final selenium approach failed: {e}")
    
    logger.error(f"Failed to fetch {url} after all attempts")
    return None

# The rest of the functions remain the same as in the original code
def extract_text_from_html(html_content):
    """Extract readable text content from HTML."""
    if not html_content:
        return ""
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove script and style elements
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()
    
    # Get text
    text = soup.get_text()
    
    # Break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    
    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    
    # Remove blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    
    return text

def extract_people_names_with_stanford(text):
    """Extract people's names from text using Stanford NER."""
    if not text:
        return set()
    
    people = set()
    
    # Tokenize the text into sentences
    for sent in sent_tokenize(text):
        # Tokenize each sentence into words
        tokens = word_tokenize(sent)
        # Tag tokens using Stanford NER
        tags = st.tag(tokens)
        # Extract names tagged as 'PERSON'
        for tag in tags:
            if tag[1] == 'PERSON':
                people.add(tag[0])
    
    return people




def extract_people_names(text, nlp):
    """Extract people's names from text using spaCy NER and Stanford NER."""
    if not text:
        return set()
    
    # Use spaCy NER
    doc = nlp(text)
    people = set()
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            people.add(ent.text)
    
    # Use Stanford NER
    stanford_people = extract_people_names_with_stanford(text)
    people.update(stanford_people)
    
    return people

def extract_names_from_static_content(content):
    """Extract people names from static content."""
    nlp = load_nlp_model()
    
    # Process the content
    names = extract_people_names(content, nlp)
    
    # Special handling for content with intro sections
    if "Hi, I'm" in content or "Hello, I'm" in content:
        intro_lines = [line for line in content.split('\n') if "Hi, I'm" in line or "Hello, I'm" in line]
        for line in intro_lines:
            # Extract name after "Hi, I'm" or "Hello, I'm"
            match = re.search(r"(?:Hi,|Hello,)\s+I'?m\s+([A-Za-z]+)", line)
            if match:
                names.add(match.group(1))
    
    return names, content

def process_file_content(file_path):
    """Read content from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return None

def detect_direct_names(text):
    """Detect names directly from text without NLP, for simple cases."""
    names = set()
    
    # Look for capitalized words that might be names
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        
        # Check for lines that might be just a name
        if len(line.split()) <= 3 and all(word[0].isupper() for word in line.split() if word and word[0].isalpha()):
            # Exclude nav items like "Home", "Projects", etc.
            if line not in ["Home", "Projects", "About", "Contact", "Services", "Products", "Blog"]:
                names.add(line)
        
        # Check for "Hi, I'm [Name]" pattern
        if "Hi, I'm" in line or "Hello, I'm" in line:
            parts = re.split(r"Hi, I'm|Hello, I'm", line)
            if len(parts) > 1:
                # Extract the first word after the pattern
                first_word = parts[1].strip().split(',')[0].split()[0]
                if first_word and first_word[0].isupper():
                    names.add(first_word)
    
    return names

def filter_valid_names(people_names):
    """Filter valid names from the set of detected names."""
    valid_names = set()
    for name in people_names:
        # Skip all-uppercase or overly long "names"
        if name.isupper() or len(name.split()) > 3:
            continue
        # Remove common non-name terms
        if name.lower() in ["home", "projects", "about", "contact", "services", "blog", "request resume", "secure password generator", "cybersecurity certification", "cybersecurity fellow", "hunter college", "new york city"]:
            continue
        # Exclude anything with numbers
        if any(char.isdigit() for char in name):
            continue
        # Ensure name length is between 5 and 20 characters
        if not (5 <= len(name) <= 20):
            continue
        # Accept names like "Prabhjott" or "John Doe"
        if re.match(r"^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*$", name):
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
        
        # Fetch the page content
        html_content = fetch_page_content(current_url)
        if not html_content:
            logger.warning(f"Failed to fetch content from {current_url}")
            continue
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract text
        text = extract_text_from_html(html_content)
        if text:
            all_text += text + "\n"
            
            # Extract people names
            names = extract_people_names(text, nlp)
            people_names.update(names)
            
            # Also try direct name detection
            direct_names = detect_direct_names(text)
            people_names.update(direct_names)
        
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
    
    logger.info(f"Crawled {len(visited_urls)} pages")
    logger.info(f"Found {len(people_names)} unique person names")
    logger.info(f"Found {len(internal_links)} internal links")
    logger.info(f"Found {len(external_links)} external links")
    
    return people_names, all_text, visited_urls, internal_links, external_links

def main():
    """Main function to parse arguments and run the crawler."""
    parser = argparse.ArgumentParser(description='Extract people names from a website or text content')
    parser.add_argument('input', help='The domain to crawl (e.g., example.com) or file containing website content')
    parser.add_argument('--max-pages', type=int, default=20, help='Maximum number of pages to crawl')
    args = parser.parse_args()
    
    try:
        # Crawl a website
        logger.info(f"Starting crawl of {args.input}")
        people_names, all_text, visited_urls, internal_links, external_links = crawl_site(args.input, args.max_pages)
        
        # Filter valid names
        valid_names = filter_valid_names(people_names)
        
        # Print results to console
        print("\nPotential Owners Found:")
        for name in sorted(valid_names):
            print(f"- {name}")
        
        print("\nInternal Links Found:")
        for url in sorted(internal_links):
            print(f"- {url}")
        
        print("\nExternal Links Found:")
        for url in sorted(external_links):
            print(f"- {url}")
        
        print("\nPages Visited:")
        print(f"- {len(visited_urls)} pages visited")
    
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()