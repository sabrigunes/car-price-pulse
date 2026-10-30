from abc import ABC, abstractmethod
import logging
from sqlalchemy.orm import Session

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)


class BaseOrchestrator(ABC):

  def __init__(self, db_session: Session, brand_name: str):
    self.db_session = db_session
    self.brand_name = brand_name
    print(f'Starting process for brand: {brand_name}.')
    self.logger = logging.getLogger(f'Orchestrator.{brand_name}')

  @abstractmethod
  def run(self):
    """Executes the entire process for the specific brand."""
    pass