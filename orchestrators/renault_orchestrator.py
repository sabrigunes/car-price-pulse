from database.crud import CarCRUD
from parsers.renault_parser import RenaultParser
from scrapers.renault_scraper import RenaultScraper
from .base_orchestrator import BaseOrchestrator


class RenaultOrchestrator(BaseOrchestrator):

  def __init__(self, db_session):
    super().__init__(db_session, brand_name="Renault")
    self.crud = CarCRUD(db_session)

  def run(self):
    self.logger.info(f"🚀 Starting {self.brand_name} price collection pipeline for all URLs...")

    try:
      # Step 1: Fetch target URLs list from DB using CRUD layer
      target_urls = self.crud.get_brand_urls(self.brand_name)
      if not target_urls:
        self.logger.error(f"❌ Target URLs could not be retrieved from DB for {self.brand_name}.")
        return

      total_saved = 0

      # Step 2: Loop through each URL using the exact same scraper and parser pipeline
      for target_url in target_urls:
        self.logger.info(f"🌐 Processing URL: {target_url}")

        scraper = RenaultScraper(target_url)
        html_content = scraper.fetch_html()

        if not html_content:
          self.logger.warning(f"⚠️ Failed to retrieve raw HTML for {target_url}. Skipping...")
          continue

        parser = RenaultParser(html_content)
        parsed_data = parser.parse()

        if not parsed_data:
          self.logger.warning(f"⚠️ Parsed data returned empty for {target_url}. Skipping...")
          continue

        self.logger.info(f"💾 Saving {len(parsed_data)} records from {target_url} via CRUD...")
        self.crud.save_scraped_items(parsed_data, brand_name=self.brand_name)
        total_saved += len(parsed_data)

      self.logger.info(f"✅ {self.brand_name} pipeline completed successfully. Total records saved: {total_saved}")

    except Exception as e:
      self.logger.error(
          f"❌ An error occurred during the {self.brand_name} pipeline: {e}",
          exc_info=True,
      )
      self.db_session.rollback()