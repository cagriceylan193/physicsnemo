"""
ADIM 1: Üç farklı sıcaklıkta örgünün neye benzediğini görelim.

  T = 1.5  (T < T_c)  -> düzenli faz: spinlerin çoğu aynı yönde (ferromanyet)
  T = 2.27 (T ≈ T_c)  -> kritik nokta: her ölçekte kümeler (fraktal görünüm)
  T = 3.5  (T > T_c)  -> düzensiz faz: rastgele, tuz-biber görüntüsü (paramanyet)

Çalıştırmak için:  python adim1_anlik_goruntu.py
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ising import T_C_KESIN, metropolis_tarama, rastgele_orgu, tohum_ayarla

L = 128
TARAMA = 2000
sicakliklar = [1.5, T_C_KESIN, 3.5]
basliklar = ["T = 1.5  (düzenli)", f"T = {T_C_KESIN:.3f}  (kritik)", "T = 3.5  (düzensiz)"]

tohum_ayarla(42)
fig, eksenler = plt.subplots(1, 3, figsize=(13, 4.6))
for ax, T, baslik in zip(eksenler, sicakliklar, basliklar):
    s = rastgele_orgu(L, seed=1)  # her sıcaklıkta rastgele başlangıç
    for _ in range(TARAMA):
        metropolis_tarama(s, T)
    m = s.mean()
    ax.imshow(s, cmap="gray", vmin=-1, vmax=1, interpolation="nearest")
    ax.set_title(f"{baslik}\nm = {m:+.3f}")
    ax.axis("off")
    print(f"T = {T:.3f}: spin başına manyetizasyon m = {m:+.3f}")

fig.suptitle(f"2B Ising modeli, {L}x{L} örgü, {TARAMA} Metropolis taraması (beyaz = +1, siyah = -1)")
fig.tight_layout(rect=(0, 0, 1, 0.92))
fig.savefig("sekil1_anlik_goruntuler.png", dpi=120)
print("Kaydedildi: sekil1_anlik_goruntuler.png")
