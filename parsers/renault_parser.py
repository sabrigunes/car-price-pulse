from parsers.base_parser import BaseParser


class RenaultParser(BaseParser):
  """Renault specific HTML parser inheriting from BaseParser."""

  def parse(self) -> list[dict]:
    results = []

    fiyat_listeleri = self.soup.find_all("fiyat-list")

    for blok in fiyat_listeleri:
      model_title_tag = blok.find("h2", class_="model-title")
      model_name = (
          model_title_tag.get_text(strip=True)
          if model_title_tag
          else "Unknown"
      )

      price_table = blok.find("table", class_="price-table")
      if not price_table:
        continue

      rows = price_table.find("tbody").find_all("tr")

      for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 2:
          variant_name = cols[0].get_text(strip=True)
          price_text = cols[1].get_text(strip=True)

          results.append({
              "model_name": model_name,
              "variant_name": variant_name,
              "price": price_text,
              "currency": "TRY",
          })

    return results