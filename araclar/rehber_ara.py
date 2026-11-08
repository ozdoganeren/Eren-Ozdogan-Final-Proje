def rehber_ara(sorgu: str, k: int = 3) -> list[dict]:
  try:
    if not sorgu or not sorgu.strip():
      return [{"hata": "Geçerli bir arama sorgusu girilmedi."}]

    rehber_metinleri = VERI.get("rehber", [])
    if not rehber_metinleri:
      return [{"hata": "Rehber veritabanı boş veya bulunamadı."}]

    sorgu_temiz = sorgu.lower().strip()
    uwan_sonuclar = []

    for item in rehber_metinleri:
      icerik = item.get("icerik", "").lower()
      baslik = item.get("baslik", "").lower()

      if sorgu_temiz in icerik or sorgu_temiz in baslik:
        uwan_sonuclar.append({
            "baslik": item.get("baslik"),
            "icerik": item.get("icerik"),
            "kaynak": item.get("kaynak", "rehber.md"),
        })

    if not uwan_sonuclar:
      return [{
          "bilgi": "Aradığınız kritere uygun rehber kaydı bulunamadı.",
          "sonuc_sayisi": 0,
      }]

    return uwan_sonuclar[:k]
  except Exception as e:
    return [{"hata": f"Rehber araması sırasında hata oluştu: {str(e)}"}]
