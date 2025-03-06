# **WhoseDomain: Advanced Domain Attribution Beyond WHOIS**

## **Overview**  
WhoseDomain is an automated system for **domain and website attribution** that goes beyond traditional WHOIS queries. WHOIS-based domain ownership identification is becoming increasingly unreliable due to privacy protection services and data redaction (e.g., GDPR). This project leverages **web scraping, TLS certificate analysis, and natural language processing (NLP)** to extract ownership information from multiple sources, providing a **more accurate and scalable** method for identifying domain owners.  

## **Features**  
- **Web Scraping for Ownership Indicators** – Extracts metadata, privacy policies, terms of service (TOS), and copyright information.  
- **TLS Certificate Analysis** – Breaks down SSL/TLS certificates to identify organizational ownership.
-  **Named Entity Recognition (NER) with NLP** – Extracts company names, email addresses, and social media links from website content.  
-  **Domain Correlation** – Links related domains using passive DNS and TLS Subject Alternative Names (SANs).  
-  **Automated Ranking Algorithm** – Prioritizes the most reliable ownership indicators while filtering out third-party references.  
-  **Attribution Graph Generation** – Provides a transparent visualization of ownership discovery.  

## **How It Works**  
### 1. **Data Collection**  
- Scrapes website metadata, privacy policies, and legal pages.  
- Extracts TLS certificates and analyzes Subject and Issuer fields.  
- Uses passive DNS and external sources to identify related domains.  

### 2. **Data Processing**  
- NLP and Named Entity Recognition (NER) extract company names and ownership indicators.  
- Filters out unrelated third-party mentions (e.g., advertisers, hosting providers).  
- Uses synonym resolution to link variations of company names.  

### 3. **Attribution & Ranking**  
- Clusters similar ownership signals.  
- Ranks the most relevant owner based on confidence scoring.  
- Outputs an **attribution graph** for verification and analysis.  

## **Installation**  
To set up and run WhoseDomain on your machine, follow these steps:  

### **Prerequisites**  
- Python 3.x  
- Pip  
- Virtual environment (optional but recommended)  

### **Clone the Repository**  
```bash
git clone https://github.com/yourusername/WhoseDomain.git
cd WhoseDomain
```

### **Install Dependencies**  
```bash
pip install -r requirements.txt
```

## **Usage**  
Run the script with a target domain:  
```bash
python whosedomain.py --domain example.com
```  

Optional arguments:  
```bash
  --domain <domain>       # The target domain to analyze  
  --depth <int>           # Depth level for subdomain exploration  
  --output <file>         # Save results to a file  
```

## **Example Output**  
```
Domain: example.com  
Detected Owner: Example Inc.  
Attribution Confidence: 92%  
Sources:  
- Privacy Policy: "Example Inc. is the data controller."  
- TLS Certificate: Issued to Example Inc.  
- WHOIS Data: Redacted  
Related Domains:  
- example.net  
- example-cdn.com  
```

## **Future Improvements**  
- Expand NLP models to support **multi-language attribution**.  
- Enhance the ranking system with **machine learning-based confidence scoring**.  
- Implement **real-time tracking** for ownership changes.  
