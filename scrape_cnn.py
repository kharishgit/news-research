# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# import json
# import time

# # Set up Selenium WebDriver
# options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Keep commented
# options.add_argument("--disable-gpu")
# options.add_argument("--no-sandbox")
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

# service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service, options=options)

# # CNN World URL
# cnn_url = "https://edition.cnn.com/world"
# driver.get(cnn_url)

# # Wait for news links to load
# try:
#     WebDriverWait(driver, 30).until(
#         EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href*='/world/']"))
#     )
#     print("News links detected.")
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(5)
#     print(f"Page source length: {len(driver.page_source)} characters")
#     with open("cnn_page.html", "w", encoding="utf-8") as f:
#         f.write(driver.page_source)
# except Exception as e:
#     print(f"Timeout waiting for news links: {e}")

# # Extract news articles
# articles = []
# link_elements = driver.find_elements(By.CSS_SELECTOR, "a[href*='/world/']")
# print(f"Found {len(link_elements)} links with '/world/'")

# for link_elem in link_elements:
#     try:
#         # Look for a nearby headline (span with class 'container__headline-text')
#         title_elem = link_elem.find_element(By.XPATH, ".//span[contains(@class, 'container__headline-text')] | .//h3 | .//h2")
#         title = title_elem.text.strip()
#         link = link_elem.get_attribute("href")
#         if title and "/world/" in link:
#             articles.append({"title": title, "link": link})
#     except:
#         continue

# # Close the browser
# driver.quit()

# # Save data to JSON
# with open("cnn_news.json", "w", encoding="utf-8") as file:
#     json.dump(articles, file, indent=4)

# print(f"✅ Found {len(articles)} CNN news articles, saved to 'cnn_news.json'")



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
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# CNN URL
cnn_url = "https://www.cnn.com"

driver.get(cnn_url)

# Wait for news links to load
try:
    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href*='/202']"))
    )
    print("News links detected.")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    with open("cnn_page.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
except Exception as e:
    print(f"Timeout waiting for news links: {e}")
    driver.quit()
    exit()

# Collect links and titles
articles = []
link_data = []
link_elements = driver.find_elements(By.CSS_SELECTOR, "a[href*='/202']")
print(f"Found {len(link_elements)} links with '/202'")

for link_elem in link_elements:
    try:
        link = link_elem.get_attribute("href")
        title_elem = link_elem.find_element(
            By.XPATH, 
            ".//h3 | .//h2 | .//span[contains(@class, 'title')] | .//div[contains(@class, 'headline')]"
        )
        title = title_elem.text.strip()
        if (title and 
            "/202" in link and 
            title.lower() not in ["", "advertisement", "live", "watch", "cnn", "home", "world", "politics"] and 
            not link.endswith("/cnn")):
            link_data.append({"title": title, "link": link})
            print(f"Collected: {title} | {link}")
    except Exception as e:
        print(f"Skipped link during collection: {e}")
        continue

# Process articles for content
for data in link_data[:10]:
    try:
        title = data["title"]
        link = data["link"]
        print(f"Processing article: {title} | {link}")
        if "live" in link.lower():
            print(f"Skipped live page: {link}")
            continue
        driver.get(link)
        content = ""
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "article p, div[class*='paragraph'], p"))
            )
            content_elems = driver.find_elements(By.CSS_SELECTOR, "article p, div[class*='paragraph'] p, p")
            content = " ".join([elem.text.strip() for elem in content_elems if elem.text.strip()])[:500]
            if not content:
                try:
                    meta_desc = driver.find_element(By.CSS_SELECTOR, "meta[name='description']")
                    content = meta_desc.get_attribute("content").strip()[:500] if meta_desc else ""
                except:
                    content = ""
            print(f"Content length: {len(content)} chars")
        except Exception as e:
            print(f"Error fetching content for {link}: {e}")
            content = ""
        articles.append({"title": title, "link": link, "content": content, "source": "CNN"})
        print(f"Saved article: {title}")
        if len(articles) >= 10:
            break
    except Exception as e:
        print(f"Error processing article {link}: {e}")
        continue

# Close the browser
driver.quit()

# Save to JSON
with open("cnn_news.json", "w", encoding="utf-8") as file:
    json.dump(articles, file, indent=4)

print(f"✅ Saved {len(articles)} CNN news articles to 'cnn_news.json'")