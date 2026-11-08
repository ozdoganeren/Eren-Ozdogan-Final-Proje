
| Test | Soru (kısa) | Hangi uzman? | Hangi araçlar? | Hangi kural/doküman? | Tuzak ne? |
|---|---|---|---|---|---|
| E01 | Kiralık Daire | ilan | `ilan_detay`, `ilan_ara` | ilanlar.json + ek_ilanlar.json | - | 
| E02 | Metroya yakın | ilan | `ilan_ara` | ilanlar.json + ek_ilanlar.json + Yakınlık 10 dakikadan az olacak | - |
| E03 | E201 peşin fiyat dışı masraf | finans | `masraf_hesapla` | parametreler.json | - |
| E04 | E203 120 ay vade ile aylık taksit | finans | `masraf_hesapla`, `kredi_hesapla` | parametreler.json | - |
| E05 | E204 %80 kredi ile satın alım | finans | `kredi_hesapla` | parametreler.json | Azami kredi oranı %50 (hayali parametre). Asistan kuralı belirtmeli, %80 hesaplamamalı. |
| E06 | E115 Kapora | ilan | `ilan_detay`, `ilan_ara`, `rehber_ara` | ilanlar.json + ek_ilanlar.json | Kapora + yurt dışı + WhatsApp + piyasanın çok altında fiyat gibi sebeplerden asistan göndermemeyi önermeli


| … | | | | | |
