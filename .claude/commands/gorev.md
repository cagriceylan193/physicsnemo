---
description: Kişisel ajanlardan birine görev ver. Kullanım - /gorev <ajan> <görev> (ajan adı verilmezse uygun olan seçilir)
argument-hint: "[takvim|arastirma|brifing|borsa|akademik|finansal|haftalik] <görev açıklaması>"
---

Kullanıcı şu görevi verdi: $ARGUMENTS

Kişisel ajanlar (.claude/agents/):
- `takvim-asistani` – takvim, planlama, toplantı saati
- `arastirma-asistani` – kaynaklı araştırma ve rapor
- `sabah-brifingi` – günün takvim + e-posta + piyasa özeti
- `borsa-ogretmeni` – borsa eğitimi ve finansal danışmanlık (eğitim amaçlı)
- `akademik-hedef-kocu` – akademik hedefler ve haftalık akademik değerlendirme
- `finansal-hedef-kocu` – parasal hedefler, bütçe ve haftalık para değerlendirmesi

`haftalik` kısaltması: önce akademik-hedef-kocu, sonra finansal-hedef-kocu ile haftalık
değerlendirmeyi sırayla yap; ikisi bittikten sonra tek bir "Haftanın özeti" ver.

Adımlar:
1. Görevin ilk kelimesi bir ajan kısaltmasıysa (takvim, arastirma, brifing, borsa, akademik, finansal, haftalik)
   o ajanı kullan; değilse görevin içeriğine en uygun ajanı seç.
   Görev birden fazla ajana dokunuyorsa sırayla çalıştır ve sonuçları birleştir.
2. Ajanı Agent aracıyla, görevi eksiksiz ve kendi başına anlaşılır biçimde yazarak başlat.
3. Ajanın sonucunu kullanıcıya Türkçe ve kısa olarak aktar; onay gerektiren bir işlem
   varsa (etkinlik oluşturma vb.) kullanıcıya sor.
