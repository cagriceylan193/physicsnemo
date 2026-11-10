# 2B Ising Modeli: Metropolis Monte Carlo ile T_c'yi bulmak

Sıfırdan başlayanlar için bir öğrenme projesi.

## Kurulum ve çalıştırma
```bash
pip install numpy matplotlib numba
python adim1_anlik_goruntu.py      # ~10 sn
python adim2_sicaklik_taramasi.py  # ~2 dk
```

## Dosyalar
| Dosya | İçerik |
|---|---|
| `ising.py` | Çekirdek: Metropolis taraması, enerji, ölçümler |
| `adim1_anlik_goruntu.py` | Üç sıcaklıkta örgünün görüntüsü (`sekil1_anlik_goruntuler.png`) |
| `adim2_sicaklik_taramasi.py` | Sıcaklık taraması ve T_c tahmini (`sekil2_faz_gecisi.png`) |

## Fizik özeti
- Hamiltonyen: `H = -J Σ s_i s_j` (en yakın komşular), `s_i = ±1`, `J = k_B = 1`.
- Kesin çözüm (Onsager 1944): `T_c = 2 / ln(1+√2) ≈ 2.2692`.
- Boltzmann dağılımından örnek almak için Metropolis kullanıyoruz: spini çevirmeyi öner,
  `min(1, e^{-ΔE/T})` olasılıkla kabul et.

## İlk sonuçlar
| Yöntem | T_c tahmini |
|---|---|
| χ tepe noktası (L = 64) | 2.325 (sonlu boyut kayması nedeniyle yüksek) |
| Binder kesişimi (16/32/64) | **≈ 2.281** (%0.5 hata) |
| Kesin değer | 2.2692 |

## Alıştırmalar (sırayla)
1. `T = 1.5` için rastgele başlangıç yerine tüm spinleri +1 alarak başlayın. Dengeye ulaşma süresi nasıl değişti?
2. `m`'yi tarama sayısına karşı çizin (zaman serisi). Dengeleme ne kadar sürüyor?
3. Ölçümlerin **otokorelasyon süresini** hesaplayın. T_c yakınında neden çok büyüyor? (kritik yavaşlama)
4. Hata çubuklarını **blok ortalaması (binning)** yöntemiyle hesaplayın.
5. Yerel Metropolis yerine **Wolff küme algoritmasını** yazın. T_c yakınındaki gürültü nasıl değişti?
6. Sonlu boyut ölçeklemesi: `χ_max ∝ L^{γ/ν}` ilişkisinden `γ/ν`'yi bulun (kesin değer 7/4).
