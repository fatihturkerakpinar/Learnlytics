import pdfplumber
import pandas as pd
from pathlib import Path

def pdf_to_csv(pdf_path: str, output_dir: str = "out/csv"):
    """PDF içeriğindeki tüm tablo verilerini tek CSV dosyasına aktarır."""
    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    all_tables = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables()
            if not tables:
                print(f"[UYARI] Sayfa {page_num} içinde tablo bulunamadı.")
                continue

            for table in tables:
                # İlk satır başlık gibi görünüyorsa düzeltelim
                if table and len(table) > 1:
                    # Sütun isimlerini benzersiz hale getir
                    columns = table[0]
                    unique_columns = []
                    for i, col in enumerate(columns):
                        if columns.count(col) > 1:
                            unique_columns.append(f"{col}_{i}")
                        else:
                            unique_columns.append(col)
                    df = pd.DataFrame(table[1:], columns=unique_columns)
                else:
                    df = pd.DataFrame(table)
                df["page_number"] = page_num
                all_tables.append(df)

    # Tüm sayfaları birleştir
    if all_tables:
        full_df = pd.concat(all_tables, ignore_index=True)
        csv_path = output_dir / f"{pdf_path.stem}.csv"
        full_df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        print(f"[BAŞARILI] CSV başarıyla kaydedildi: {csv_path}")
        return full_df
    else:
        print("[HATA] PDF içinde tablo bulunamadı.")
        return pd.DataFrame()

# 🔹 Örnek kullanım
if __name__ == "__main__":
    pdf_to_csv("GÜNEŞLİ BİL KURS - AKTİF TG.pdf")
