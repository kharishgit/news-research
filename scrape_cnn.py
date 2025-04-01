from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Keep commented
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# CNN World URL
cnn_url = "https://edition.cnn.com/world"
driver.get(cnn_url)

# Wait for news links to load
try:
    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href*='/world/']"))
    )
    print("News links detected.")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    print(f"Page source length: {len(driver.page_source)} characters")
    with open("cnn_page.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
except Exception as e:
    print(f"Timeout waiting for news links: {e}")

# Extract news articles
articles = []
link_elements = driver.find_elements(By.CSS_SELECTOR, "a[href*='/world/']")
print(f"Found {len(link_elements)} links with '/world/'")

for link_elem in link_elements:
    try:
        # Look for a nearby headline (span with class 'container__headline-text')
        title_elem = link_elem.find_element(By.XPATH, ".//span[contains(@class, 'container__headline-text')] | .//h3 | .//h2")
        title = title_elem.text.strip()
        link = link_elem.get_attribute("href")
        if title and "/world/" in link:
            articles.append({"title": title, "link": link})
    except:
        continue

# Close the browser
driver.quit()

# Save data to JSON
with open("cnn_news.json", "w", encoding="utf-8") as file:
    json.dump(articles, file, indent=4)

print(f"✅ Found {len(articles)} CNN news articles, saved to 'cnn_news.json'")