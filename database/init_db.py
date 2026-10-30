from database.connection import DatabaseManager
from database.schemas import Base  # schemas.py içerisindeki DeclarativeBase / Base tanımı


class DatabaseInitializer:
    def __init__(self):
        # DatabaseManager örneğini sınıf içinde başlatıyoruz
        self.db_manager = DatabaseManager()

    def create_tables(self):
        """Connects to the database and creates all tables defined in the models."""
        print("🔄 Establishing database connection and creating tables...")

        try:
            # Tüm modelleri (schemas.py içinde Base'den türeyen tabloları) veritabanına basıyoruz
            Base.metadata.create_all(bind=self.db_manager.engine)
            print(
                "✅ Success: All database tables (brands, models, variants, price_history) have been successfully created!")
        except Exception as e:
            print(f"❌ Error: An issue occurred while creating tables -> {e}")


if __name__ == "__main__":
    # Sınıftan bir nesne üretip tablo oluşturma metodunu tetikliyoruz
    initializer = DatabaseInitializer()
    initializer.create_tables()