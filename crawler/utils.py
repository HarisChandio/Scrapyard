import time

from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from info_scrapper.settings import (
  CHROME_OPTIONS,
  SEARCH_PAGES,

)

chrome_options = webdriver.ChromeOptions(); [chrome_options.add_argument(option) for option in CHROME_OPTIONS]
def get_driver():
    """Creates a driver instance without using a context manager"""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def extract_element_text(parent, selector, attribute="text", default="N/A"):
    """Helper function to extract text or attribute from a WebElement."""
    try:
        element = parent.find_element(By.CSS_SELECTOR, selector)
        return element.text if attribute == "text" else element.get_attribute(attribute)
    except:
        return default

def google_search(query, duration, location):
  print('[INFO] Starting Google Search')
  main_driver = None
  try:
      print("[DEBUG] Searching:", query)
      enhanced_query = f'{query} {location}'
      #enhanced_query = enhance_search_query(enhanced_query)
      print("[DEBUG] Enhanced query:", enhanced_query)

      main_driver = get_driver()
      main_driver.get("https://www.google.com")

      WebDriverWait(main_driver, 10).until(
          EC.presence_of_element_located((By.NAME, "q"))
      )
      search_box = main_driver.find_element(By.NAME, "q")
      search_box.send_keys(enhanced_query)
      search_box.send_keys(Keys.RETURN)

      WebDriverWait(main_driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.MjjYud")))
      print("[DEBUG] Fetched results.")

      results = []
      print(f"[DEBUG] Search duration: {duration} minutes")

      for page in range(5):  # Adjust page range as necessary
          print(f"[DEBUG] Fetching results from page {page}")

          try:
              search_results = main_driver.find_elements(By.CSS_SELECTOR, "div.MjjYud")
              for result in search_results:
                  try:

                      href = extract_element_text(result, "a", "href", "No URL")
                      title = extract_element_text(result, "h3.LC20lb.MBeuO.DKV0Md", "text", "No title")
                      website = extract_element_text(result, "span.VuuXrf", "text", "No website")
                      description = extract_element_text(result, "div.VwiC3b span", "text", "No description")

                      # Append the result
                      results.append({
                          "title": title,
                          "url": href,
                          "website": website,
                          "description": description
                      })
                  except Exception as e:
                      print(f"[ERROR] Error extracting a result: {e}")

          except Exception as e:
              print(f"[ERROR] Error on page {page}: {e}")
              break

      results = list(set(results))
      print(f"[DEBUG] Unique search results found: {len(results)}")

      return results

  except Exception as e:
    print(f"[ERROR IN GOOGLE SEARCH] Error: {e}")
  finally:
    if main_driver:
      main_driver.quit()

  return results