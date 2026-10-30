import time
from scrapers.base_scraper import SeleniumScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class RenaultScraper(SeleniumScraper):
  """Renault specific scraper focusing purely on fetching raw HTML from a given URL."""

  def __init__(self, url: str):
    super().__init__(url)

  def fetch_html(self) -> str:
    """Connects to the provided URL, handles interactions, and returns raw HTML."""
    try:
      print(f"🌐 Connecting to target URL: {self.url}")
      self.driver.get(self.url)

      WebDriverWait(self.driver, 15).until(
          EC.presence_of_element_located((By.TAG_NAME, "body"))
      )
      print("✅ Base page structure loaded successfully.")

      delay = 3
      print(f"💤 {delay} seconds delay...")
      time.sleep(delay)

      html_content = self.driver.page_source
      print(
          f"✅ Fetch successful! Total HTML length: {len(html_content)}"
          " characters."
      )
      return html_content

    except Exception as e:
      print(f"❌ Selenium Error: {e}")
      raise
    finally:
      if self.driver:
        self.driver.quit()