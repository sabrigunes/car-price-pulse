from sqlalchemy.orm import Session
from database.schemas import Brand, Model, Variant, PriceHistory
import logging

logger = logging.getLogger("Database.CRUD")


class CarCRUD:
    def __init__(self, db_session: Session):
        self.db = db_session

    from sqlalchemy.dialects import \
        postgresql  # SQLite kullanıyorsanız sqlite dialect import edilebilir ama str() genelde yeterlidir.

    def get_brand_urls(self, brand_name: str) -> list[str]:
        """Reads and returns a list of target URLs for a specific brand from the database, split by comma."""
        brand = self.db.query(Brand).filter_by(name=brand_name).first()

        if brand and brand.url:
            # Virgülle ayrılmış URL'leri liste haline getirelim
            urls = [u.strip() for u in brand.url.split(",") if u.strip()]
            print(f"✅ Found {len(urls)} URLs for {brand_name}")
            return urls

        print(f"❌ Brand '{brand_name}' found, but 'url' attribute is missing or empty.")
        return []
    
    def get_or_create_brand(self, brand_name: str) -> Brand:
        brand = self.db.query(Brand).filter_by(name=brand_name).first()
        if not brand:
            logger.info(f"Creating new Brand: {brand_name}")
            brand = Brand(name=brand_name)
            self.db.add(brand)
            self.db.commit()
            self.db.refresh(brand)
        return brand

    def get_or_create_model(self, brand_id: int, model_name: str) -> Model:
        model = self.db.query(Model).filter_by(brand_id=brand_id, name=model_name).first()
        if not model:
            logger.info(f"Creating new Model: {model_name} (Brand ID: {brand_id})")
            model = Model(brand_id=brand_id, name=model_name)
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
        return model

    def get_or_create_variant(self, model_id: int, variant_name: str, year: int = 2026, **kwargs) -> Variant:
        variant = self.db.query(Variant).filter_by(model_id=model_id, name=variant_name).first()
        if not variant:
            logger.info(f"Creating new Variant: {variant_name}")
            variant = Variant(
                model_id=model_id,
                name=variant_name,
                year=year,
                engine=kwargs.get("engine"),
                transmission=kwargs.get("transmission"),
                drive_train=kwargs.get("drive_train"),
                extra_specs=kwargs.get("extra_specs")
            )
            self.db.add(variant)
            self.db.commit()
            self.db.refresh(variant)
        return variant

    def create_price_history(self, variant_id: int, price: float, currency: str = "TRY"):
        price_entry = PriceHistory(
            variant_id=variant_id,
            price=price,
            currency=currency
        )
        self.db.add(price_entry)
        self.db.commit()
        return price_entry

    def save_scraped_items(self, parsed_data: list, brand_name: str = "Renault"):
        brand = self.get_or_create_brand(brand_name)

        for item in parsed_data:
            model_name = item.get("model_name")
            variant_name = item.get("variant_name")
            raw_price = item.get("price")

            year = item.get("year", 2026)
            engine = item.get("engine")
            transmission = item.get("transmission")
            drive_train = item.get("drive_train")
            extra_specs = item.get("extra_specs")

            if not model_name or not variant_name or not raw_price:
                logger.warning(f"Skipping incomplete item: {item}")
                continue

            clean_price = (
                str(raw_price)
                .replace("₺", "")
                .replace(".", "")
                .replace(",", ".")
                .strip()
            )
            try:
                price_val = float(clean_price)
            except ValueError:
                price_val = 0.0

            model = self.get_or_create_model(brand.id, model_name)
            variant = self.get_or_create_variant(
                model_id=model.id,
                variant_name=variant_name,
                year=year,
                engine=engine,
                transmission=transmission,
                drive_train=drive_train,
                extra_specs=extra_specs
            )
            self.create_price_history(
                variant_id=variant.id,
                price=price_val,
                currency=item.get("currency", "TRY")
            )

        logger.info(f"Successfully saved {len(parsed_data)} items for {brand_name}.")