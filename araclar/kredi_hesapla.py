def kredi_hesapla(ilan_id: str, kredi_orani: float, vade_ay: int) -> dict:
  try:
    no = str(ilan_id).upper().replace(" ", "")
    ilanlar = {i["id"]: i for i in VERI.get("ilanlar", [])}
    ilan = ilanlar.get(no)

    if not ilan:
      return {"hata": f"{no} numaralı ilan bulunamadı."}

    if ilan.get("tip", "").lower() != "satilik":
      return {"hata": "Kredi hesaplaması sadece satılık ilanlar için yapılabilir."}

    AZAMI_VADE = 120
    if vade_ay > AZAMI_VADE:
      return {
          "hata": "Vade sınırı aşıldı",
          "kural": f"Yasal azami konut kredisi vadesi {AZAMI_VADE} aydır.",
      }

    fiyat = ilan.get("fiyat", 0)
    ana_para = fiyat * 0.80

    r = kredi_orani
    n = vade_ay

    if r == 0:
      taksit = ana_para / n
    else:
      carpim = (1 + r) ** n
      taksit = (ana_para * r * carpim) / (carpim - 1)

    toplam_odeme = taksit * n

    return {
        "id": no,
        "cekilen_tutar": round(ana_para, 2),
        "aylik_taksit": round(taksit, 2),
        "toplam_odeme": round(toplam_odeme, 2),
        "vade_ay": vade_ay,
    }
  except Exception as e:
    return {"hata": f"Kredi hesaplama hatası: {str(e)}"}
