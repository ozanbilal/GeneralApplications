import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

def stress_strain_steel(epsilon, fy, Es):
    """
    Çelik için gerilme-deformasyon ilişkisi.
    :param epsilon: Deformasyon
    :param fy: Akma mukavemeti (MPa)
    :param Es: Elastisite modülü (MPa)
    :return: Gerilme (MPa)
    """
    ey = fy / Es  # Akma deformasyonu
    if abs(epsilon) < ey:
        return Es * epsilon
    else:
        return fy * np.sign(epsilon)

def stress_strain_concrete(epsilon, fc):
    """
    Beton için gerilme-deformasyon ilişkisi.
    :param epsilon: Deformasyon
    :param fc: Beton mukavemeti (MPa)
    :return: Gerilme (MPa)
    """
    ec = 0.002  # Beton için kırılma deformasyonu
    if abs(epsilon) < ec:
        return fc * (2 * epsilon/ec - (epsilon/ec)**2)
    else:
        return 0

def calculate_section_capacity(b, h, fc, fy, cover, bar_diameter, num_bars):
    """
    Betonarme kesit kapasitesini daha gerçekçi hesaplar.
    """
    Es = 200000  # Çelik için elastisite modülü (MPa)
    d = h - cover - bar_diameter / 2
    As = np.pi * (bar_diameter / 2) ** 2 * num_bars  # Donatı alanı

    def moment_curvature(phi):
        c = d / (0.003 / phi + fy / Es)
        a = phi * c
        fs = stress_strain_steel(a - d, fy, Es)
        fc = stress_strain_concrete(a, fc)
        M = As * fs * (d - a / 2) + 0.85 * fc * b * a * (d - a / 3)
        return M

    curvatures = np.linspace(0, 0.02, 50)  # Örnek eğrilik değerleri
    moments = [moment_curvature(phi) for phi in curvatures]

    return curvatures, moments

# Kesit parametreleri ve hesaplama
b = 30  # cm
h = 50  # cm
fc = 25  # MPa
fy = 420  # MPa
cover = 3  # cm
bar_diameter = 3.2  # cm
num_bars = 8  # Donatı sayısı

curvatures, moments = calculate_section_capacity(b, h, fc, fy, cover, bar_diameter, num_bars)

# Diyagramı çiz
plt.figure(figsize=(10, 5))
plt.plot(curvatures, moments, label='Moment-Krivatür')
plt.title('Moment-Krivatür Diyagramı')
plt.xlabel('Krivatür (1/cm)')
plt.ylabel('Moment (kNm)')
plt.legend()
plt.grid(True)
plt.show()
