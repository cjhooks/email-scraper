# Import necessary libraries
from bs4 import BeautifulSoup  # For parsing HTML and extracting information
import requests  # For sending HTTP requests to web pages
import requests.exceptions  # For handling exceptions related to HTTP requests
import urllib.parse  # For parsing and manipulating URLs
from collections import deque  # For creating a queue to manage URLs during the scan
import re  # For using regular expressions to find email patterns

# Function to scan for emails from a given URL
def scan_emails():
    # Prompt the user to input the target URL to scan
    user_url = str(input('[+] Enter Target URL To Scan: '))
    
    # Initialize a deque (double-ended queue) with the user's URL as the first element
    urls = deque([user_url])
    
    # Set to keep track of already scraped URLs (to avoid duplicate work)
    scraped_urls = set()
    
    # Set to store unique email addresses found during the scan
    emails = set()
    
    # Counter to limit the number of URLs processed
    count = 0
    
    try:
        # Start processing URLs from the queue
        while len(urls):
            count += 1  # Increment the counter for each processed URL
            
            # Stop processing after 100 URLs (safety limit to avoid infinite loops)
            if count == 100:
                break
            
            # Get the next URL from the queue
            url = urls.popleft()
            
            # Add the current URL to the set of scraped URLs
            scraped_urls.add(url)
            
            # Parse the URL to extract its components (e.g., scheme, netloc, path)
            parts = urllib.parse.urlsplit(url)
            
            # Construct the base URL (e.g., https://example.com)
            base_url = '{0.scheme}://{0.netloc}'.format(parts)
            
            # Get the directory path of the URL (e.g., https://example.com/folder/)
            path = url[:url.rfind('/')+1] if '/' in parts.path else url
            
            # Display the URL being processed
            print('[%d] Processing %s' % (count, url))
            
            try:
                # Send an HTTP GET request to fetch the content of the URL
                response = requests.get(url)
            except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
                # Skip the URL if it is invalid or inaccessible
                continue
            
            # Use a regular expression to find all email addresses in the response text
            new_emails = set(re.findall(
                r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+",  # Regex pattern for emails
                response.text,  # Search the page content
                re.I  # Case-insensitive matching
            ))
            
            # Add the newly found emails to the set of all emails
            emails.update(new_emails)
            
            # Use BeautifulSoup to parse the HTML content of the page
            soup = BeautifulSoup(response.text, features="lxml")
            
            # Find all anchor tags (<a>) in the HTML to extract hyperlinks
            for anchor in soup.find_all("a"):
                # Get the 'href' attribute (the hyperlink) from the anchor tag
                link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
                
                # Convert relative URLs (e.g., "/about") to absolute URLs
                if link.startswith('/'):
                    link = base_url + link
                # Handle links without a protocol (e.g., "example.html")
                elif not link.startswith('http'):
                    link = path + link
                
                # Add the new link to the queue if it's not already processed or in the queue
                if not link in urls and not link in scraped_urls:
                    urls.append(link)
    except KeyboardInterrupt:
        # Gracefully exit the program when the user presses Ctrl+C
        print('[-] Closing!')

    # Display all the unique emails found
    if emails:
        for mail in emails:
            print(mail)  # Print each email on a new line
    else:
        # Inform the user if no emails were found
        print("[!] No emails found.")

    # Prompt the user to decide what to do next
    user_choice = input("\nWould you like to search a new domain or close the program? (new/close): ").lower()
    if user_choice == 'new':
        # Recursively call the function to start a new scan
        scan_emails()
    else:
        # Exit the program
        print("Goodbye!")

# Start the email scanning program
scan_emails()
