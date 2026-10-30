import logging
from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class BaseScraper(ABC):
    """Abstract base class for all scrapers, handling fetch strategy."""

    def __init__(self, url: str):
        self.url = url

    @abstractmethod
    def fetch_html(self) -> str:
        """Must be implemented to fetch raw HTML using the selected strategy."""
        pass


class SeleniumScraper(BaseScraper):
    """For dynamic JavaScript-heavy websites or sites with bot protections using Selenium."""

    def __init__(self, url: str):
        super().__init__(url)
        self.driver = self._init_driver()

    def _init_driver(self):
        """Initializes and configures the Selenium WebDriver."""
        options = Options()
        # options.add_argument("--headless=new")  # Uncomment for headless mode
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        logging.info("Initializing Selenium WebDriver...")
        driver = webdriver.Chrome(options=options)
        return driver

    @abstractmethod
    def fetch_html(self) -> str:
        pass