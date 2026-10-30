from datetime import datetime, UTC
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base, relationship

# SQLAlchemy 2.0 uyumlu Base sınıfı
Base = declarative_base()

class Brand(Base):
    """Represents car brands (e.g., Ford, BMW, Toyota)."""
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    url = Column(String(255))
    created_at = Column(DateTime, default=datetime.now())

    # Relationships
    models = relationship("Model", back_populates="brand", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Brand(id={self.id}, name='{self.name}')>"


class Model(Base):
    """Represents car models belonging to a brand (e.g., Focus, Corolla)."""
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, autoincrement=True)
    brand_id = Column(Integer, ForeignKey("brands.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    brand = relationship("Brand", back_populates="models")
    variants = relationship("Variant", back_populates="car_model", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Model(id={self.id}, name='{self.name}')>"


class Variant(Base):
    """Represents specific trim/hardware packages with technical specs."""
    __tablename__ = "variants"

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(Integer, ForeignKey("models.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(150), nullable=False)          # e.g., "1.5L EcoBoost Active"
    year = Column(Integer, nullable=False)          # e.g., 2026
    engine = Column(String(100), nullable=True)         # e.g., "1.5L Petrol", "Electric"
    transmission = Column(String(50), nullable=True)    # e.g., "Automatic", "Manual"
    drive_train = Column(String(50), nullable=True)     # e.g., "FWD", "AWD", "4x4"
    extra_specs = Column(JSONB, nullable=True)          # Flexible JSON storage for accessory/equipment data
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    car_model = relationship("Model", back_populates="variants")
    price_histories = relationship("PriceHistory", back_populates="variant", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Variant(id={self.id}, name='{self.name}')>"


class PriceHistory(Base):
    """Time-series table to track price changes of vehicle variants over time."""
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    variant_id = Column(Integer, ForeignKey("variants.id", ondelete="CASCADE"), nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String(10), default="TRY")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    variant = relationship("Variant", back_populates="price_histories")

    def __repr__(self):
        return f"<PriceHistory(id={self.id}, variant_id={self.variant_id}, price={self.price})>"