import sys
import os
import json

# Proje kök dizinini modül arama yoluna ekliyoruz
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from database.connection import DatabaseManager
from database.schemas import Brand
from scrapers.renault_scraper import RenaultScraper
from parsers.renault_parser import RenaultParser


def get_renault_url_from_db():
    """Veritabanından Renault markasının URL'sini dinamik olarak çeker."""
    db_manager = DatabaseManager()
    session = db_manager.get_session()
    try:
        brand = session.query(Brand).filter(Brand.name == "Renault").first()
        if brand and hasattr(brand, 'url') and brand.url:
            return brand.url
        # Eğer henüz veritabanında URL sütunu dolu değilse varsayılan URL'yi döner
        return "https://www.renault.com.tr/fiyat-listesi.html"
    finally:
        session.close()


def run_live_test():
    print("🚀 Canlı test süreci başlatılıyor...")

    # 1. Adım: URL'yi al
    url = get_renault_url_from_db()
    print(f"🔍 Hedef URL: {url}")

    try:
        # 2. Adım: Selenium Scraper ile canlı HTML verisini çek
        print("🌐 Selenium ile web sitesine bağlanılıyor ve HTML alınıyor...")
        scraper = RenaultScraper(url)
        raw_html = scraper.fetch_html()
        with open("renault_debug.html", "w", encoding="utf-8") as f:
            f.write(raw_html)
        print("🔍 Ham HTML 'renault_debug.html' dosyasına kaydedildi. İnceleyebilirsin.")
        print(f"✅ Ham HTML başarıyla alındı. Uzunluk: {len(raw_html)} karakter.")

        # 3. Adım: Renault Parser ile HTML'i anlamlandır / ayrıştır
        print("⚙️ HTML içeriği RenaultParser ile ayrıştırılıyor...")
        parser = RenaultParser(raw_html)
        parsed_data = parser.parse()

        # 4. Adım: Sonuçları ekrana yazdır
        if parsed_data:
            print(f"\n🎉 Başarılı! Toplam {len(parsed_data)} adet varyant/fiyat bilgisi bulundu:\n")
            print(json.dumps(parsed_data, indent=4, ensure_ascii=False))
        else:
            print("⚠️ Uyarı: Sayfa çekildi ancak fiyat tablosu ayrıştırılamadı. HTML yapısı değişmiş olabilir.")

    except Exception as e:
        print(f"❌ Test sırasında bir hata oluştu: {e}")


if __name__ == "__main__":
    run_live_test()