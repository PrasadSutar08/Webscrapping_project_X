from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from datetime import datetime
import uuid

# MongoDB configuration
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "twitter_trends"
COLLECTION_NAME = "trends"

# ChromeDriver path
CHROMEDRIVER_PATH = r"C:\Drivers\chromedriver-win64\chromedriver.exe"  # Update this with your ChromeDriver path

# Twitter login credentials
TWITTER_USERNAME = "PrasadSutar08"  # Replace with your Twitter username
TWITTER_PASSWORD = "Prasad##123"  # Replace with your Twitter password

def fetch_twitter_trends():
    options = webdriver.ChromeOptions()
    # Optional: Disable automation detection
    # options.add_argument('--headless')  # Remove this line to run with UI visible
    options.add_argument('--disable-gpu')  # Disable GPU for smoother execution
    options.add_argument('--no-sandbox')  # Disable sandboxing for Linux environments
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)

    try:
        # Log in to Twitter (formerly Twitter X)
        driver.get("https://x.com/i/flow/login?lang=en")

        # Wait for username field to appear and input username
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.NAME, "text")))
        username_input = driver.find_element(By.NAME, "text")
        username_input.send_keys(TWITTER_USERNAME)
        username_input.send_keys(Keys.RETURN)

        # Wait for password field and input password
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.NAME, "password")))
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys(TWITTER_PASSWORD)
        password_input.send_keys(Keys.RETURN)

        # Wait for the homepage to load
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//nav")))

        # Navigate directly to Trending section
        trending_url = "https://x.com/explore/tabs/trending"
        driver.get(trending_url)

        # Wait for the Trending section to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-testid='trend']"))
        )

        # Scroll down to ensure all elements are loaded
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Fetch trend names
        trend_elements = driver.find_elements(By.XPATH, "//div[@data-testid='trend']//span[not(contains(text(),'Trending')) and not(contains(text(),'·'))]")
        trend_names = [trend.text.strip() for trend in trend_elements if trend.text.strip()]

        # Get top 5 trends
        top_5_trends = trend_names[:5]

        # Debugging print
        print("Fetched Trends:", top_5_trends)

        # Generate unique ID and record the end time
        unique_id = str(uuid.uuid4())
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save to MongoDB
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
        record = {
            "_id": unique_id,
            "trends": top_5_trends,  # Limit to top 5 trends
            "end_time": end_time,
        }
        collection.insert_one(record)

        return record

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    finally:
        driver.quit()

if __name__ == "__main__":
    result = fetch_twitter_trends()
    if result:
        print("Trending Topics Fetched:", result)
    else:
        print("Failed to fetch trending topics.")
