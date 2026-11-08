# EvBul Satın Alma Rehberi
## Satın alma masrafları
Konut alırken satış fiyatı dışında masraflar oluşur: tapu harcı, döner sermaye ücreti, emlak ofisi hizmet bedeli (ofis aracılığıyla alınıyorsa), zorunlu deprem sigortası (DASK) ve kredi kullanılıyorsa ekspertiz ücreti. Bu projede kullanılan oranlar veri/parametreler.json dosyasındadır ve eğitim amaçlı sadeleştirilmiştir.
## Tapu harcı
Tapu harcı satış bedeli üzerinden alıcı ve satıcı için ayrı ayrı hesaplanır. Bu projede alıcı payı yüzde 2 kabul edilmiştir.
## Konut kredisi
Kredi tutarı konut değerinin belirli bir oranını geçemez. Aylık taksit, eşit taksitli kredi formülü ile hesaplanır. Bu projede faiz oranı, azami vade ve azami kredi oranı parametreler.json dosyasındadır; gerçek oranlar bankaya ve döneme göre değişir.
## Tapu kontrolü
Satın almadan önce tapu kaydı resmi kanallardan doğrulanmalı, üzerinde ipotek, haciz veya şerh olup olmadığı kontrol edilmelidir. Satıcı tapu sahibi değilse noter onaylı vekaletname istenmelidir.
