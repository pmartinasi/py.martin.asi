import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time, sys, random

# Set to keep track of visited URLs
visited_urls = set()

def crawl_website(url, max_depth=256, depth=0):
    if depth > max_depth or url in visited_urls:
        print("url in visited_urls = " + str(url in visited_urls))
        print("depth (" + str(depth) + ") > max_depth(256) = " + str(depth > max_depth))
        print(str(url) + " not processed")
        return
    else:
        md = max_depth
    
        random_seconds = random.randint(1, 8)
        print("waiting " + str(random_seconds) + " seconds for the next URL: " + str(url))
        time.sleep(random_seconds)
    try:
        # Fetch the content from the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        # Add the URL to the visited set
        visited_urls.add(url)

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get text content
        text_content = soup.get_text(separator='\n', strip=True)

        # Save to a .txt file
        filename = url.replace('http://', '').replace('https://', '').replace('/', '_') + ".txt"
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(text_content)

        print(f"Content saved to {filename}")

        # Find and crawl all links on the page
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(url, href)
            crawl_website(full_url, md, depth + 1)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL {url}: {e}")
        pass
    except:
        pass
        

if __name__ == "__main__":
    #url_to_crawl = input("Enter the URL to crawl: ")
    #crawl_website(url_to_crawl)
    
    if len(sys.argv) != 2:
        print("Usage: python script.py <URL>")
        sys.exit(1)

    url_to_crawl = sys.argv[1]
    crawl_website(url_to_crawl)