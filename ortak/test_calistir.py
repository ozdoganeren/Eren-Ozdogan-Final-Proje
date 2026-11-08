"""
Ortak test çalıştırıcı — tüm projelerde AYNI betik kullanılır.
Eğitmen gizli testleri de bu betikle çalıştıracaktır; bu yüzden ARAYÜZ SÖZLEŞMESİNE uymanız zorunludur.

ARAYÜZ SÖZLEŞMESİ
-----------------
Sisteminiz şu imzaya sahip bir fonksiyon sunmalıdır:

    def cevapla(mesaj: str, oturum: dict) -> dict:
        ...
        return {
            "ajan": "siparis",        # cevabı üreten uzman ajanın KISA adı (proje README'sinde tanımlı).
                                      # Birden fazla uzman çalıştıysa "+" ile birleştirin: "siparis+menu"
            "cevap": "...",           # kullanıcıya giden son metin
            "iz": [...],              # (opsiyonel) araç çağrıları: [{"arac": ..., "girdi": ..., "gozlem": ...}]
        }

- `oturum` bir sözlüktür. Çok turlu testlerde AYNI sözlük her turda tekrar verilir; hafızanızı burada tutun.
- Bazı testler oturumu dolu başlatır (ör. {"rol": "aday", "aday_id": "A04"}). Bu bilgiler SİSTEM tarafından
  verilmiştir; kullanıcı mesajından değil buradan okunmalıdır.

KULLANIM (Colab)
----------------
    !wget -q https://raw.githubusercontent.com/istanbuldatascienceacademy/ai-architect-/main/final-proje/ortak/test_calistir.py
    from test_calistir import testleri_calistir
    sonuc = testleri_calistir(cevapla, "testler/acik_testler.json", "test_sonuclari/acik_testler.csv")
"""
import json, re, time, csv, os, traceback

def tr_kucult(s):
    return re.sub(r"\s+", " ", str(s).replace("I", "ı").replace("İ", "i").lower()).strip()

def _ajan_dogru_mu(beklenen, gelen):
    if beklenen == "*":
        return True
    beklenenler = beklenen if isinstance(beklenen, list) else [beklenen]
    gelenler = [a.strip() for a in str(gelen).split("+")]
    return any(b in gelenler for b in beklenenler)

def _icerik_kontrol(t, cevap):
    c, sorunlar = tr_kucult(cevap), []
    for x in t.get("icermeli", []):
        if tr_kucult(x) not in c: sorunlar.append(f"eksik: '{x}'")
    if t.get("herhangi") and not any(tr_kucult(x) in c for x in t["herhangi"]):
        sorunlar.append(f"şunlardan hiçbiri yok: {t['herhangi']}")
    for x in t.get("icermemeli", []):
        if tr_kucult(x) in c: sorunlar.append(f"olmamalıydı: '{x}'")
    if t.get("herhangi_k"):
        liste, k = t["herhangi_k"]["liste"], t["herhangi_k"]["k"]
        bulunan = [x for x in liste if tr_kucult(x) in c]
        if len(bulunan) < k: sorunlar.append(f"{liste} içinden en az {k} tanesi olmalı, bulunan: {bulunan}")
    return sorunlar

def testleri_calistir(cevapla, test_dosyasi, cikti_csv=None, ayrintili=True):
    testler = json.load(open(test_dosyasi, encoding="utf-8"))
    satirlar = []
    for t in testler:
        oturum = dict(t.get("oturum", {}))
        mesajlar = t.get("konusma") or [t["soru"]]
        t0, hata = time.time(), None
        try:
            for m in mesajlar:
                r = cevapla(m, oturum)
            ajan, cevap = r.get("ajan", ""), r.get("cevap", "")
        except Exception as e:
            ajan, cevap, hata = "", "", f"{type(e).__name__}: {e}"
            if ayrintili: traceback.print_exc()
        sure = time.time() - t0
        a_ok = _ajan_dogru_mu(t["beklenen_ajan"], ajan) and not hata
        sorunlar = [hata] if hata else _icerik_kontrol(t, cevap)
        c_ok = not sorunlar
        satirlar.append({"id": t["id"], "tur": t.get("tur", "normal"), "ajan_dogru": a_ok, "icerik_dogru": c_ok,
                         "gecti": a_ok and c_ok, "beklenen_ajan": json.dumps(t["beklenen_ajan"], ensure_ascii=False),
                         "gelen_ajan": ajan, "sorunlar": " | ".join(sorunlar), "sure_sn": round(sure, 1),
                         "soru": " ⟶ ".join(mesajlar), "cevap": cevap})
        if ayrintili:
            print(f"{'✅' if a_ok and c_ok else '❌'} {t['id']} [{t.get('tur','normal')}] ajan:{'✓' if a_ok else '✗'}({ajan}) içerik:{'✓' if c_ok else '✗'}"
                  + (f"  → {'; '.join(sorunlar)}" if sorunlar else ""))
    n = len(satirlar)
    ozet = {"test_sayisi": n,
            "gecen": sum(s["gecti"] for s in satirlar),
            "ajan_dogrulugu": round(sum(s["ajan_dogru"] for s in satirlar) / n, 3),
            "icerik_dogrulugu": round(sum(s["icerik_dogru"] for s in satirlar) / n, 3),
            "ortalama_sure_sn": round(sum(s["sure_sn"] for s in satirlar) / n, 1),
            "tur_bazinda": {}}
    for tur in sorted({s["tur"] for s in satirlar}):
        grup = [s for s in satirlar if s["tur"] == tur]
        ozet["tur_bazinda"][tur] = f"{sum(s['gecti'] for s in grup)}/{len(grup)}"
    if cikti_csv:
        os.makedirs(os.path.dirname(cikti_csv) or ".", exist_ok=True)
        with open(cikti_csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(satirlar[0].keys())); w.writeheader(); w.writerows(satirlar)
    if ayrintili:
        print(f"\nGEÇEN: {ozet['gecen']}/{n} | Ajan doğruluğu: {ozet['ajan_dogrulugu']:.0%} | İçerik doğruluğu: {ozet['icerik_dogrulugu']:.0%} "
              f"| Ort. süre: {ozet['ortalama_sure_sn']} sn | Tür bazında: {ozet['tur_bazinda']}")
    return {"ozet": ozet, "satirlar": satirlar}


if __name__ == "__main__":
    # Betiğin kendisini sınamak için sahte bir sistem: python test_calistir.py <test_dosyasi>
    import sys
    def sahte(mesaj, oturum):
        oturum.setdefault("n", 0); oturum["n"] += 1
        return {"ajan": "politika", "cevap": f"Sahte cevap {oturum['n']}: {mesaj}"}
    testleri_calistir(sahte, sys.argv[1])
