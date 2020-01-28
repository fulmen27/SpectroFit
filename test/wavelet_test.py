"""import pywt
import numpy as np
import matplotlib.pyplot as plt
t = np.linspace(-1, 1, 200, endpoint=False)
sig  = np.cos(2 * np.pi * 7 * t) + np.real(np.exp(-7*(t-0.4)**2)*np.exp(1j*2*np.pi*2*(t-0.4)))
plt.plot(t, sig)
plt.show()
widths = np.arange(1, 31)
cwtmatr, freqs = pywt.cwt(sig, widths, 'mexh')
print(cwtmatr)
print(freqs)
plt.imshow(cwtmatr, extent=[-1, 1, 1, 31], cmap='PRGn', aspect='auto',
           vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())  # doctest: +SKIP
plt.show() # doctest: +SKIP"""

import numpy as np
import matplotlib.pyplot as plt

import pywt
import pywt.data

t = [i for i in range(100)]
t = np.asarray(t)
sig = np.cos(2 * np.pi / 7 * t) + np.cos(2 * np.pi / 50 * t) - np.cos(2 * np.pi / 4 * t) + np.cos(2 * np.pi / 2 * t)

"""
ca, cd = pywt.dwt(sig, "bior3.5")
cd_0 = [0 for _ in range(len(cd))]
ca_0 = [0 for _ in range(len(ca))]
sig_ret = pywt.idwt(ca, cd_0, "bior3.5")
sig_ret2 = pywt.idwt(ca_0, cd, "bior3.5")"""

coeffs = pywt.wavedec(sig, "rbio6.8", level=3)
print(pywt.wavelist('rbio'))
print(len(coeffs))
coeffs[3] = np.asarray([0 for i in range(len(coeffs[3]))])
coeffs[2] = np.asarray([0 for i in range(len(coeffs[2]))])
coeffs[1] = np.asarray([0 for i in range(len(coeffs[1]))])
# coeffs[0] = np.asarray([0 for i in range(len(coeffs[0]))])
sig_ret = pywt.waverec(coeffs, "rbio6.8")

# plt.plot(t, sig)
plt.plot(t, sig_ret)
# plt.plot(t, np.cos(2 * np.pi / 7 * t))
plt.plot(t, np.cos(2 * np.pi / 50 * t))
# plt.plot(t, - np.cos(2 * np.pi / 4 * t))
# plt.plot(t, np.cos(2 * np.pi / 2 * t))
plt.show()