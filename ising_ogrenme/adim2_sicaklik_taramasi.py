"""
ADIM 2: Sıcaklığı tarayıp T_c'yi bulalım.

Farklı örgü boyutlarında (L = 16, 32, 64) her sıcaklık için m, chi, C ve Binder kümülantı U ölçülür.

T_c'yi iki yolla tahmin ediyoruz:
  (a) Alınganlık chi'nin tepe noktası: L büyüdükçe T_c'ye yaklaşır (ama sonlu boyut kayması var).
  (b) Binder kümülantının kesişimi: U_L(T) eğrileri farklı L'ler için yaklaşık tek bir noktada,
      T_c'de kesişir. Bu yöntem sonlu boyut etkisine çok daha az duyarlıdır -> daha doğru.

Çalıştırmak için:  python adim2_sicaklik_taramasi.py   (birkaç dakika sürebilir)
"""

import time

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from ising import T_C_KESIN, gozlemlenebilirler, rastgele_orgu, simule_et, tohum_ayarla

BOYUTLAR = [16, 32, 64]
DENGELEME = 2000  # her sıcaklıkta ölçmeden önce yapılan tarama sayısı
OLCUM = 20000  # ölçüm alınan tarama sayısı
# Geniş aralıkta seyrek, T_c civarında sık nokta:
SICAKLIKLAR = np.unique(
    np.concatenate([np.linspace(1.5, 3.5, 11), np.linspace(2.15, 2.40, 11)])
)

tohum_ayarla(123)
sonuclar = {}
for L in BOYUTLAR:
    N = L * L
    t0 = time.time()
    s = rastgele_orgu(L, seed=L)
    satirlar = []
    # Yüksek sıcaklıktan düşüğe doğru gidiyoruz ("tavlama"): her sıcaklık bir öncekinin
    # son durumundan başlar, böylece dengeye daha çabuk ulaşır.
    for T in SICAKLIKLAR[::-1]:
        m, e = simule_et(s, T, DENGELEME, OLCUM)
        satirlar.append((T, gozlemlenebilirler(m, e, T, N)))
    satirlar.reverse()
    sonuclar[L] = {
        "T": np.array([r[0] for r in satirlar]),
        **{k: np.array([r[1][k] for r in satirlar]) for k in ["m", "chi", "C", "U", "e"]},
    }
    print(f"L = {L:3d} bitti ({time.time() - t0:.1f} s)")

# ---- (a) Alınganlık tepesinden T_c tahmini ----
print("\n(a) Alınganlık (chi) tepe noktası:")
for L in BOYUTLAR:
    r = sonuclar[L]
    print(f"   L = {L:3d}:  T_tepe = {r['T'][np.argmax(r['chi'])]:.3f}")


# ---- (b) Binder kesişiminden T_c tahmini ----
def kesisim(r1, r2):
    """İki U(T) eğrisinin farkının işaret değiştirdiği yeri doğrusal interpolasyonla bulur."""
    T, fark = r1["T"], r1["U"] - r2["U"]
    pencere = (T > 2.1) & (T < 2.45)  # sadece kritik bölgeye bak
    T, fark = T[pencere], fark[pencere]
    for k in range(len(T) - 1):
        if fark[k] * fark[k + 1] < 0:
            return T[k] - fark[k] * (T[k + 1] - T[k]) / (fark[k + 1] - fark[k])
    return np.nan


print("\n(b) Binder kümülantı kesişimleri:")
tahminler = []
for L1, L2 in [(16, 32), (32, 64), (16, 64)]:
    Tx = kesisim(sonuclar[L1], sonuclar[L2])
    tahminler.append(Tx)
    print(f"   L = {L1:2d} & {L2:2d}:  T_c ≈ {Tx:.4f}")
Tc_tahmin = np.nanmean(tahminler)
print(f"\nOrtalama Binder tahmini: T_c ≈ {Tc_tahmin:.4f}")
print(f"Kesin (Onsager) değer:   T_c = {T_C_KESIN:.4f}")
print(f"Bağıl hata: {abs(Tc_tahmin - T_C_KESIN) / T_C_KESIN * 100:.2f} %")

# ---- Grafikler ----
fig, eks = plt.subplots(2, 2, figsize=(11, 8))
basliklar = {
    "m": "Manyetizasyon  ⟨|m|⟩",
    "e": "Spin başına enerji  ⟨e⟩",
    "chi": "Manyetik alınganlık  χ",
    "U": "Binder kümülantı  U",
}
for ax, anahtar in zip(eks.flat, ["m", "e", "chi", "U"]):
    for L in BOYUTLAR:
        r = sonuclar[L]
        ax.plot(r["T"], r[anahtar], "o-", ms=3.5, label=f"L = {L}")
    ax.axvline(T_C_KESIN, color="k", ls="--", lw=1, label=f"Onsager T_c = {T_C_KESIN:.3f}")
    ax.set_xlabel("Sıcaklık T  (J / k_B)")
    ax.set_title(basliklar[anahtar])
    ax.grid(alpha=0.3)
eks[1, 1].set_xlim(2.1, 2.45)
eks[1, 1].set_ylim(0.45, 0.68)
eks[1, 1].axvline(Tc_tahmin, color="r", ls=":", lw=1.5, label=f"Binder tahmini = {Tc_tahmin:.3f}")
eks[1, 1].legend(fontsize=8)
eks[0, 0].legend(fontsize=8)
fig.suptitle("2B Ising modeli: Metropolis Monte Carlo ile faz geçişi")
fig.tight_layout()
fig.savefig("sekil2_faz_gecisi.png", dpi=120)
print("\nKaydedildi: sekil2_faz_gecisi.png")
