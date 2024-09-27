from selenium import webdriver
from selenium.webdriver.edge.service import Service
from bs4 import BeautifulSoup
import json
import time
import html
import requests

# Function to check if an image URL is accessible
def is_image_accessible(url):
    """Check if the image URL is accessible."""
    try:
        response = requests.head(url, allow_redirects=True)
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"Error checking image URL: {e}")
        return False

# Setup the service and driver for Microsoft Edge
service = Service(executable_path="msedgedriver.exe")  # Ensure this path is correct
driver = webdriver.Edge(service=service)

# Open UFC's trending page
driver.get("https://www.ufc.com/trending/all")

time.sleep(5)  # Let the page load fully

# Get the page source
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# Find the main container
try:
    main_container = soup.find('div', class_='trending-page-grid trending-page')
    
    # Debugging: Check if main_container is found
    if main_container is None:
        print("Main container not found.")
        driver.quit()
        exit()

    # Initialize a list to store the news data
    news_data = []

    # Find all the news items (assuming they're in 'a' tags within 'div' elements)
    news_items = main_container.find_all('a')

    if not news_items:
        print("No news items found.")
        driver.quit()
        exit()

    for item in news_items:
        link = "https://www.ufc.com" + item['href']  # Build the full link
        title = item.get_text(strip=True)  # Get the text (title of the news)

        # Debugging: Print title and link
        print(f"Title: {title}")
        print(f"Link: {link}")

        # Extract the image URL (assuming it's in 'img' tag inside the 'a' tag)
        img_tag = item.find('img')
        img_url = img_tag['src'] if img_tag else None
        
        # Fix image URL if it's a relative path
        if img_url and img_url.startswith("/"):
            img_url = "https://dmxg5wxfqgb4u.cloudfront.net" + img_url

        # Check if the image URL is accessible
        if img_url and not is_image_accessible(img_url):
            print(f"Access denied for image URL: {img_url}. Using placeholder image.")
            img_url = "https://www.mmawiki.org/it/wp-content/uploads/2012/07/ufc.jpg"  # Placeholder image URL

        # Debugging: Print image URL
        print(f"Image URL: {img_url}")

        # Clean and decode the title
        title = html.unescape(title)  # Decode HTML entities (e.g., &amp;, &quot:)
        title = title.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')

        # Append the news item data to the list
        news_data.append({
            'title': title,
            'link': link,
            'image': img_url,
            'video_url': item.get('data-video-url', None)  # Add video URL if available
        })

except Exception as e:
    print(f"An error occurred: {e}")

# Save the data to a JSON file
with open("news.json", "w", encoding="utf-8") as file:
    json.dump(news_data, file, ensure_ascii=False, indent=4)

print("News data saved to 'news.json'.")

# Quit the browser
driver.quit()
