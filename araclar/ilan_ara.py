def ilan_ara(
    tip: str | None = None,
    il: str | None = None,
    ilceler: list[str] | None = None,
    mahalle: str | None = None,
    oda: str | None = None,
    min_fiyat: float | None = None,
    max_fiyat: float | None = None,
    evcil_hayvan: bool | None = None,
    esyali: bool | None = None,
    max_metro_dk: int | None = None,
    serbest_metin: str | None = None,
    sirala: str = "fiyat_artan",
    limit: int = 5,
) -> dict:
  try:
    ilanlar = VERI.get("ilanlar", [])
    filtrelenen = []

    temiz_tip = tip.strip().lower() if tip else None
    temiz_il = il.strip().lower() if il else None
    temiz_ilceler = (
        [i.strip().lower() for i in ilceler] if ilceler else None
    )
    temiz_mahalle = mahalle.strip().lower() if mahalle else None
    temiz_oda = oda.strip().lower() if oda else None
    temiz_metin = (
        serbest_metin.strip().lower() if serbest_metin else None
    )

    for ilan in ilanlar:
      if temiz_tip and ilan.get("tip", "").lower() != temiz_tip:
        continue
      if temiz_il and ilan.get("il", "").lower() != temiz_il:
        continue
      if temiz_ilceler:
        ilan_ilce = ilan.get("ilce", "").lower()
        if not any(i in ilan_ilce for i in temiz_ilceler):
          continue
      if temiz_mahalle and ilan.get("mahalle", "").lower() != temiz_mahalle:
        continue
      if temiz_oda and ilan.get("oda", "").lower() != temiz_oda:
        continue
      if min_fiyat and ilan.get("fiyat", 0) < min_fiyat:
        continue
      if max_fiyat and ilan.get("fiyat", 0) > max_fiyat:
        continue
      if evcil_hayvan is not None and ilan.get("evcil_hayvan") != evcil_hayvan:
        continue
      if esyali is not None and ilan.get("esyali") != esyali:
        continue
      if (
          max_metro_dk is not None
          and ilan.get("metroya_yurume_dk", 999) > max_metro_dk
      ):
        continue
      if temiz_metin:
        aciklama = ilan.get("aciklama", "").lower()
        if temiz_metin not in aciklama:
          continue

      filtrelenen.append(ilan)

    if not filtrelenen:
      return {
          "sonuc_sayisi": 0,
          "ilanlar": [],
          "oneri": (
              "Kriterlere uygun ilan bulunamadı. Fiyatı biraz artırabilir veya"
              " filtreleri esnetebilirsiniz."
          ),
      }

    if sirala == "fiyat_artan":
      filtrelenen.sort(key=lambda x: x.get("fiyat", 0))
    elif sirala == "fiyat_azalan":
      filtrelenen.sort(key=lambda x: x.get("fiyat", 0), reverse=True)

    ozet_ilanlar = [
        {
            "id": i.get("id"),
            "ilce": i.get("ilce"),
            "mahalle": i.get("mahalle"),
            "oda": i.get("oda"),
            "m2": i.get("m2"),
            "fiyat": i.get("fiyat"),
            "tip": i.get("tip"),
        }
        for i in filtrelenen[:limit]
    ]

    return {"sonuc_sayisi": len(filtrelenen), "ilanlar": ozet_ilanlar}
  except Exception as e:
    return {"hata": f"Arama sırasında hata oluştu: {str(e)}"}