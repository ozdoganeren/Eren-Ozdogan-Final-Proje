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

---

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

---

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

---

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

---

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

---

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

---

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
