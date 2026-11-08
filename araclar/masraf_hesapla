def masraf_hesapla(ilan_id: str, kredi_kullanilacak_mi: bool = False) -> dict:
  try:
    no = str(ilan_id).upper().replace(" ", "")
    ilanlar = {i["id"]: i for i in VERI.get("ilanlar", [])}
    ilan = ilanlar.get(no)

    if not ilan:
      return {"hata": f"{no} numaralı ilan bulunamadı."}

    fiyat = ilan.get("fiyat", 0)
    durum = ilan.get("tip", "satilik").lower()
    ilan_veren = ilan.get("ilan_veren", "").lower()

    kalemler = {}
    toplam = 0.0

    if durum == "satilik":
      tapu_harci = fiyat * 0.02
      kalemler["tapu_harci_alici"] = tapu_harci
      toplam += tapu_harci

      if ilan_veren == "emlakçı":
        komisyon_kdvli = fiyat * 0.02 * 1.20
        kalemler["emlak_komisyonu_kdv_dahil"] = komisyon_kdvli
        toplam += komisyon_kdvli

      if kredi_kullanilacak_mi:
        ekspertiz = 5000.0
        kalemler["ekspertiz_ucreti"] = ekspertiz
        toplam += ekspertiz

    elif durum == "kiralik":
      depozito = fiyat * 2
      kalemler["depozito_ust_siniri"] = depozito
      toplam += depozito

      if ilan_veren == "emlakçı":
        ofis_bedeli = fiyat * 1.20
        kalemler["ofis_bedeli_kdv_dahil"] = ofis_bedeli
        toplam += ofis_bedeli

      kalemler["ilk_ay_kira"] = fiyat
      toplam += fiyat

      aidat = ilan.get("aidat", 0)
      if aidat:
        kalemler["ilk_ay_aidat"] = aidat
        toplam += aidat

    return {
        "id": no,
        "tip": durum,
        "kalemler": kalemler,
        "toplam_masraf": round(toplam, 2),
    }
  except Exception as e:
    return {"hata": f"Masraf hesaplanamadı: {str(e)}"}
