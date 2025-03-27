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

def extract_people_names(text, nlp):
    """Extract people's names from text using spaCy NER and custom patterns."""
    if not text:
        return set()
    
    # Run spaCy NER
    doc = nlp(text)
    people = set()
    
    # Get names identified by the NER model
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            people.add(ent.text)
    
    # Add custom pattern recognition for names
    # Look for patterns like "I'm [NAME]" or "Hi, I'm [NAME]"
    name_patterns = [
        r"I'm\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
        r"Hi,\s+I'm\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
        r"Hello,\s+I'm\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
        r"My\s+name\s+is\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
        r"Hi,\s*I'?m\s+([A-Z][a-z]+)"  # More relaxed pattern
    ]
    
    for pattern in name_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            people.add(match.strip())
    
    # Look for standalone names that are repeated multiple times
    name_candidates = {}
    words = re.findall(r'\b([A-Z][a-z]{2,})\b', text)
    for word in words:
        if word not in ["The", "This", "That", "These", "Those", "Their", "They", "When", "Where", "What", "Which"]:
            name_candidates[word] = name_candidates.get(word, 0) + 1
    
    # Names likely appear multiple times
    for name, count in name_candidates.items():
        if count >= 2:
            people.add(name)
    
    # Look for single name on a line by itself
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if re.match(r'^[A-Z][a-z]+$', line) and len(line) > 2:
            people.add(line)
    
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

def crawl_site(domain, max_pages=20):
    """Crawl a website and collect text content and people names."""
    domain = normalize_url(domain)
    visited_urls = set()
    to_visit = {domain}
    all_text = ""
    people_names = set()
    
    nlp = load_nlp_model()
    
    logger.info(f"Starting crawl of {domain}")
    
    # Attempt crawling with increased robustness
    retry_count = 0
    use_cloudscraper = True  # Start with cloudscraper
    
    while to_visit and len(visited_urls) < max_pages and retry_count < 5:  # Increased retry count
        if not to_visit:
            retry_count += 1
            logger.warning(f"No URLs to visit, retry {retry_count}/5")
            if retry_count >= 5:
                break
            # Try the domain again as a last resort
            to_visit = {domain}
            # Toggle between scraping methods on retries
            use_cloudscraper = not use_cloudscraper
            continue
            
        current_url = to_visit.pop()
        
        if current_url in visited_urls:
            continue
        
        logger.info(f"Processing {current_url}")
        visited_urls.add(current_url)
        
        # Try to get the content with the appropriate method
        html_content = fetch_page_content(current_url, retry_count=5, use_cloudscraper=use_cloudscraper)
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
            
            # Extract more internal links to visit
            internal_links = set()
            base_domain = extract_domain(domain)
            
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                full_url = urljoin(current_url, href)
                
                if extract_domain(full_url) == base_domain:
                    internal_links.add(full_url)
            
            logger.info(f"Found {len(internal_links)} internal links")
            to_visit.update(link for link in internal_links if link not in visited_urls)
        else:
            logger.warning(f"No text content found in {current_url}")
    
    if not people_names and all_text:
        # If no names found but we have text, try again with custom patterns
        people_names = extract_people_names(all_text, nlp)
        direct_names = detect_direct_names(all_text)
        people_names.update(direct_names)
    
    logger.info(f"Crawled {len(visited_urls)} pages")
    logger.info(f"Found {len(people_names)} unique person names")
    
    return people_names, all_text, visited_urls

def main():
    """Main function to parse arguments and run the crawler."""
    parser = argparse.ArgumentParser(description='Extract people names from a website or text content')
    parser.add_argument('input', help='The domain to crawl (e.g., example.com) or file containing website content')
    parser.add_argument('--max-pages', type=int, default=20, help='Maximum number of pages to crawl')
    parser.add_argument('--output', help='Output file for the results', default='names.txt')
    parser.add_argument('--file', action='store_true', help='Treat input as a file path containing website content')
    parser.add_argument('--text', action='store_true', help='Treat input as direct text content')
    parser.add_argument('--static', action='store_true', help='Process input as static website content pasted directly')
    parser.add_argument('--use-selenium', action='store_true', help='Use Selenium WebDriver for rendering JavaScript')
    parser.add_argument('--use-cloudscraper', action='store_true', help='Use cloudscraper to bypass protections')
    
    args = parser.parse_args()
    
    try:
        if args.file:
            # Process file containing website content
            logger.info(f"Processing file: {args.input}")
            content = process_file_content(args.input)
            if not content:
                logger.error("Could not read file content")
                return
            
            people_names, all_text = extract_names_from_static_content(content)
            # Also try direct name detection
            direct_names = detect_direct_names(content)
            people_names.update(direct_names)
            visited_urls = []
        elif args.text or args.static:
            # Direct text input (e.g., piped from stdin)
            if args.input == '-':
                content = sys.stdin.read()
            else:
                content = args.input
            
            logger.info("Processing direct text input")
            people_names, all_text = extract_names_from_static_content(content)
            # Also try direct name detection
            direct_names = detect_direct_names(content)
            people_names.update(direct_names)
            visited_urls = []
        else:
            # Crawl a website
            logger.info(f"Starting crawl of {args.input}")
            people_names, all_text, visited_urls = crawl_site(args.input, args.max_pages)
        
        # If no names found but we have text, try with more aggressive patterns
        if not people_names and all_text:
            # Look for names in specific contexts
            lines = all_text.split('\n')
            for i, line in enumerate(lines):
                if "Hi, I'm" in line or "Hello, I'm" in line:
                    # Extract name after greeting
                    match = re.search(r"(?:Hi,|Hello,)\s+I'?m\s+([A-Za-z]+)", line)
                    if match:
                        people_names.add(match.group(1))
                
                # Look for standalone names
                if len(line.strip().split()) == 1 and line.strip() and line.strip()[0].isupper():
                    # Check if this might be a name
                    if len(line.strip()) > 2 and line.strip().isalpha():
                        people_names.add(line.strip())
        
        # Manual check for specific patterns in the content
        # Extract lines that might contain a name by themselves
        lines = all_text.split('\n')
        for line in lines:
            line = line.strip()
            # Check for lines that are 1-3 words and all start with uppercase
            if len(line.split()) <= 3 and len(line.split()) > 0:
                if all(word[0].isupper() for word in line.split() if word and len(word) > 0 and word[0].isalpha()):
                    # Make sure it's not a menu item
                    if not any(keyword in line.lower() for keyword in ["home", "about", "contact", "projects", "blog", "services"]):
                        people_names.add(line)
        
        # Check for text patterns that often introduce names
        greeting_patterns = [
            r"Hi,\s+I'?m\s+([A-Za-z]+)",
            r"Hello,\s+I'?m\s+([A-Za-z]+)",
            r"I\s+am\s+([A-Za-z]+\s+[A-Za-z]+)",
            r"My\s+name\s+is\s+([A-Za-z]+\s+[A-Za-z]+)"
        ]
        
        for pattern in greeting_patterns:
            matches = re.findall(pattern, all_text, re.IGNORECASE)
            for match in matches:
                people_names.add(match.strip())
        
        # Write results to file
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(f"# People found\n\n")
            if people_names:
                for name in sorted(people_names):
                    f.write(f"- {name}\n")
            else:
                f.write("No names found\n")
            
            if visited_urls:
                f.write(f"\n\n# Pages crawled ({len(visited_urls)}):\n")
                for url in sorted(visited_urls):
                    f.write(f"- {url}\n")
        
        logger.info(f"Results written to {args.output}")
        
        # Print results to console
        if people_names:
            print(f"\nFound {len(people_names)} people:")
            for name in sorted(people_names):
                print(f"- {name}")
        else:
            print("\nNo names found in the content")
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()