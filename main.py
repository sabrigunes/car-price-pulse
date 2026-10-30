from database.connection import DatabaseManager  # Kendi DatabaseManager sınıfınızı import edin
from orchestrators.renault_orchestrator import RenaultOrchestrator
from database.schemas import Base  # veya şemalarınızın olduğu yer


def run_pipeline():
    print("🚀 Live test and DB recording process is starting...")

    # DatabaseManager üzerinden PostgreSQL bağlantısını ve session'ı başlatıyoruz
    db_manager = DatabaseManager()

    # İsteğe bağlı: Tabloları kontrol et / oluştur
    Base.metadata.create_all(db_manager.engine)

    # Session alıyoruz
    session = db_manager.SessionLocal()

    try:
        RenaultOrchestrator(session).run()

    except Exception as e:
        print(f"❌ An error occurred: {e}")
        session.rollback()
    finally:
        session.close()
        print("🔒 Database connection closed.")


if __name__ == "__main__":
    run_pipeline()