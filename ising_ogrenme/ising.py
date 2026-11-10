"""
2B Ising modeli - Metropolis algoritması (çekirdek fonksiyonlar)

Model:
    H = -J * sum_<i,j> s_i * s_j      (s_i = +1 veya -1, sadece en yakın komşular)
    J = 1 ve k_B = 1 alıyoruz, yani sıcaklık T enerji birimiyle ölçülüyor.

Kesin (Onsager, 1944) kritik sıcaklık:
    T_c = 2 / ln(1 + sqrt(2)) ≈ 2.269185
"""

import numpy as np
from numba import njit

T_C_KESIN = 2.0 / np.log(1.0 + np.sqrt(2.0))


def rastgele_orgu(L, seed=0):
    """L x L boyutunda, her spini rastgele +1 veya -1 olan bir örgü üretir."""
    rng = np.random.default_rng(seed)
    return rng.choice(np.array([-1, 1], dtype=np.int8), size=(L, L))


@njit(cache=True)
def tohum_ayarla(seed):
    """Numba'nın kendi rastgele sayı üretecini başlatır (tekrarlanabilirlik için)."""
    np.random.seed(seed)


@njit(cache=True)
def metropolis_tarama(s, T):
    """
    Bir "Monte Carlo taraması" (sweep): ortalama olarak her spini bir kez çevirmeyi dener.

    Her deneme için:
      1) Rastgele bir spin seç.
      2) Onu çevirirsek enerji ne kadar değişir? -> dE = 2 * s_i * (komşuların toplamı)
      3) dE <= 0 ise çevir (enerji düşüyor, her zaman kabul).
         dE > 0 ise exp(-dE/T) olasılıkla çevir (ısıl dalgalanma).
    Periyodik sınır koşulu: kenardaki spinin komşusu karşı kenardadır (örgü bir simit/torus).
    """
    L = s.shape[0]
    # dE sadece 4 veya 8 olabilir (dE>0 durumları için); exp'i önceden hesapla -> hız
    kabul4 = np.exp(-4.0 / T)
    kabul8 = np.exp(-8.0 / T)
    for _ in range(L * L):
        i = np.random.randint(L)
        j = np.random.randint(L)
        komsu_toplami = (
            s[(i + 1) % L, j] + s[(i - 1) % L, j] + s[i, (j + 1) % L] + s[i, (j - 1) % L]
        )
        dE = 2 * s[i, j] * komsu_toplami
        if dE <= 0:
            s[i, j] = -s[i, j]
        elif dE == 4:
            if np.random.random() < kabul4:
                s[i, j] = -s[i, j]
        else:  # dE == 8
            if np.random.random() < kabul8:
                s[i, j] = -s[i, j]


@njit(cache=True)
def toplam_enerji(s):
    """H = -sum s_i s_j. Her bağı bir kez saymak için sadece sağ ve alt komşuya bakıyoruz."""
    L = s.shape[0]
    E = 0.0
    for i in range(L):
        for j in range(L):
            E -= s[i, j] * (s[(i + 1) % L, j] + s[i, (j + 1) % L])
    return E


@njit(cache=True)
def simule_et(s, T, dengeleme, olcum):
    """
    Önce `dengeleme` kadar tarama yapıp sistemi dengeye getirir (bu kısım ölçülmez),
    sonra `olcum` tarama boyunca her taramadan sonra spin başına m ve e kaydeder.
    """
    N = s.shape[0] * s.shape[1]
    for _ in range(dengeleme):
        metropolis_tarama(s, T)
    m_dizi = np.empty(olcum)
    e_dizi = np.empty(olcum)
    for k in range(olcum):
        metropolis_tarama(s, T)
        m_dizi[k] = s.sum() / N  # spin başına manyetizasyon
        e_dizi[k] = toplam_enerji(s) / N  # spin başına enerji
    return m_dizi, e_dizi


def gozlemlenebilirler(m, e, T, N):
    """
    Ölçüm dizilerinden fiziksel büyüklükleri hesaplar.
      |m|  : ortalama mutlak manyetizasyon (düzen parametresi)
      chi  : manyetik alınganlık   = N * (<m^2> - <|m|>^2) / T
      C    : özgül ısı             = N * (<e^2> - <e>^2) / T^2
      U    : Binder kümülantı      = 1 - <m^4> / (3 <m^2>^2)
    Not: Sonlu örgüde sistem +m ile -m arasında gidip gelebilir, bu yüzden |m| kullanıyoruz.
    """
    m_abs = np.abs(m)
    m2 = np.mean(m**2)
    m4 = np.mean(m**4)
    return {
        "m": np.mean(m_abs),
        "chi": N * (m2 - np.mean(m_abs) ** 2) / T,
        "C": N * (np.mean(e**2) - np.mean(e) ** 2) / T**2,
        "U": 1.0 - m4 / (3.0 * m2**2),
        "e": np.mean(e),
    }
