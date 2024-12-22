# Email Scraper with BeautifulSoup

## Overview
This Python script allows you to scrape email addresses from a given URL. It uses the `requests` library to fetch webpages, `BeautifulSoup` to parse HTML content, and `re` (regular expressions) to extract email patterns. The script also handles dynamic elements such as links, forms, iframes, and scripts to ensure a comprehensive search for email addresses.

---

## Features
- Fetches a webpage and extracts email addresses.
- Recursively follows links to explore additional pages.
- Handles elements like forms, iframes, and scripts to find hidden email sources.
- Avoids re-scraping URLs by maintaining a set of visited pages.
- Stops after processing 100 URLs to prevent excessive looping.
- Allows the user to interrupt the process safely (using `Ctrl+C`).

---

## Prerequisites
- Python 3.6 or higher.
- Install the required libraries:
  ```bash
  pip install beautifulsoup4 requests
  ```

---

## How It Works
1. **Input the Target URL**: The user provides the starting URL to scan.
2. **Parse and Process**: The script parses the webpage and extracts:
   - Email addresses via regular expressions.
   - Links, forms, iframes, and scripts for further exploration.
3. **Avoid Duplication**: Tracks processed URLs to prevent revisits.
4. **Interrupt Safely**: Allows the user to terminate the process with `Ctrl+C`.
5. **Output Emails**: Returns a set of all extracted email addresses.

---

## Code Walkthrough

### 1. Import Necessary Libraries
```python
from bs4 import BeautifulSoup
import requests
import urllib.parse
import re
from collections import deque
```
- **BeautifulSoup**: Parses HTML content.
- **requests**: Sends HTTP requests to fetch webpage content.
- **urllib.parse**: Handles URL parsing and reconstruction.
- **re**: Searches for email patterns using regular expressions.
- **deque**: Efficiently handles the list of URLs to process.

---

### 2. Function: `scan_emails`
This function scans a webpage and extracts email addresses while exploring additional links.

#### Input
- A URL provided by the user.

#### Process
- **Initialization**:
  - `urls`: A queue to track URLs to process.
  - `scraped_urls`: A set to avoid revisiting URLs.
  - `emails`: A set to store unique email addresses.

- **URL Parsing**:
  ```python
  parts = urllib.parse.urlsplit(url)
  base_url = '{0.scheme}://{0.netloc}'.format(parts)
  ```
  Breaks down the URL to extract the base (e.g., `https://example.com`).

- **HTML Parsing**:
  ```python
  soup = BeautifulSoup(response.text, features="lxml")
  ```
  Parses the HTML content for links, forms, iframes, and scripts.

- **Email Extraction**:
  ```python
  new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
  emails.update(new_emails)
  ```
  Finds all email-like patterns in the page content.

- **Exploring Additional Links**:
  Iterates over links (`<a>`), forms (`<form>`), iframes (`<iframe>`), and scripts (`<script>`), appending them to the queue if not already visited.

#### Output
- A set of unique email addresses found during the scan.

---

### 3. Safe Exit
The script allows the user to interrupt the process safely:
```python
except KeyboardInterrupt:
    print("Canceled by user")
```

---

## Example Usage
Run the script in your Python environment:
```python
emails = scan_emails('https://www.example.com')
print(emails)
```

When executed:
- The script processes the provided URL and extracts email addresses.
- It follows links, forms, iframes, and scripts to find hidden emails.

---

## Limitations
- **100-URL Limit**: Stops after processing 100 URLs to prevent infinite loops.
- **Dynamic Content**: Doesn't handle JavaScript-rendered content; for such cases, tools like Selenium may be required.
- **Error Handling**: Minimal error handling for malformed or inaccessible URLs.

---

## Installation and Running
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/email-scraper.git
   cd email-scraper
   ```

2. Install dependencies:
   ```bash
   pip install beautifulsoup4 requests
   ```

3. Run the script:
   ```bash
   python email_scraper.py
   ```

---

## Contribution
Feel free to fork this repository, open issues, or submit pull requests to improve functionality.

---

## License
This project is open-source and available under the MIT License.
