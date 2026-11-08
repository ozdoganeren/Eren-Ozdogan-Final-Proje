def ilan_risk_kontrol(ilan_id: str) -> dict:
  try:
    no = str(ilan_id).upper().replace(" ", "")
    ilanlar = {i["id"]: i for i in VERI.get("ilanlar", [])}
    ilan = ilanlar.get(no)

    if not ilan:
      return {"hata": f"{no} numaralı ilan bulunamadı."}

    tetiklenen_kurallar = []
    aciklama = ilan.get("aciklama", "").lower()

    if "kapora" in aciklama or "ön ödeme" in aciklama:
      tetiklenen_kurallar.append(
          "Açıklamada kapora veya ön ödeme talebi geçiyor."
      )
    if "yurt dışındayım" in aciklama or "kargo ile" in aciklama:
      tetiklenen_kurallar.append("Şüpheli uzaktan teslim hikayesi tespit edildi.")

    ilce = ilan.get("ilce")
    tip = ilan.get("tip")
    fiyat = ilan.get("fiyat", 0)

    benzer_fiyatlar = [
        i["fiyat"]
        for i in ilanlar.values()
        if i.get("ilce") == ilce
        and i.get("tip") == tip
        and i.get("id") != no
    ]

    if benzer_fiyatlar:
      ortalama_fiyat = sum(benzer_fiyatlar) / len(benzer_fiyatlar)
      if fiyat < (ortalama_fiyat * 0.40):
        tetiklenen_kurallar.append(
            f"Fiyat, benzer ilan ortalamasının ({ortalama_fiyat:,.0f} TL) çok"
            " altında (Piyasa anomalisi)."
        )

    risk_seviyesi = "düşük"
    if len(tetiklenen_kurallar) >= 2:
      risk_seviyesi = "yüksek"
    elif len(tetiklenen_kurallar) == 1:
      risk_seviyesi = "orta"

    return {
        "id": no,
        "risk": risk_seviyesi,
        "tetiklenen_kurallar": tetiklenen_kurallar,
    }
  except Exception as e:
    return {"hata": f"Risk kontrolü yapılamadı: {str(e)}"}
