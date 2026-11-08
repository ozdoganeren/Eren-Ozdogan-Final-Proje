def ilan_detay(ilan_id: str) -> dict:
  try:
    no = str(ilan_id).upper().replace(" ", "")
    ilanlar = {i["id"]: i for i in VERI.get("ilanlar", [])}
    ilan = ilanlar.get(no)

    if not ilan:
      return {"hata": f"{no} numaralı ilan bulunamadı."}

    return ilan
  except Exception as e:
    return {"hata": f"İlan detayları alınamadı: {str(e)}"}
