from abc import ABC, abstractmethod
from bs4 import BeautifulSoup


class BaseParser(ABC):
    """Abstract base class for parsing raw HTML into structured car pricing data."""

    def __init__(self, html_content: str):
        self.soup = BeautifulSoup(html_content, 'html.parser')

    @abstractmethod
    def parse(self) -> list[dict]:
        """Parses the HTML content and returns a standardized list of dictionaries.

        Example return format:
        [
            {
                "model_name": "Focus",
                "variant_name": "1.5L EcoBoost Active",
                "engine": "1.5L",
                "transmission": "Automatic",
                "price": 1250000.0,
                "currency": "TRY"
            },
            ...
        ]
        """
        pass