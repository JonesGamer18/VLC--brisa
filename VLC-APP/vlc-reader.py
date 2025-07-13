import spidev
import time
import numpy as np
from scipy.fft import rfft, rfftfreq

SAMPLING_RATE = 2000     
BUFFER_SIZE = 4000         
VREF = 3.3              
MAG_MIN_THRESHOLD = 3000   

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

def ler_tensao_protegida():
    dados = spi.xfer2([0x00, 0x00])
    valor = ((dados[0] & 0x1F) << 7) | (dados[1] >> 1)
    return min(valor, 4095)

def normalizar_sinal(sinal):
    return sinal - np.mean(sinal)

def detectar_frequencia():
    buffer = np.zeros(BUFFER_SIZE)
    indice = 0

    print("Coletando sinal para detecÃ§Ã£o de frequÃªncia...")

    while indice < BUFFER_SIZE:
        buffer[indice] = ler_tensao_protegida()
        indice += 1
        time.sleep(1 / SAMPLING_RATE)

    sinal_normalizado = normalizar_sinal(buffer)

    n = len(sinal_normalizado)
    yf = rfft(sinal_normalizado)
    xf = rfftfreq(n, 1 / SAMPLING_RATE)
    magnitudes = np.abs(yf)
    magnitudes[0] = 0 

    indices_validos = np.where(xf >= 200)[0]
    if len(indices_validos) == 0:
        return 0

    idx_max = indices_validos[np.argmax(magnitudes[indices_validos])]
    freq_dominante = xf[idx_max]

    min_freq = 175
    larg_canal = 50
    b = (freq_dominante - min_freq) // larg_canal
    canal_freq = int(min_freq + larg_canal / 2 + b * larg_canal)

    return canal_freq

import atexit
@atexit.register
def cleanup():
    spi.close()
    print("\nSPI finalizado.")
