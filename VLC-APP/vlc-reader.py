import spidev
import time
import numpy as np
from scipy.fft import rfft, rfftfreq

SAMPLING_RATE = 2000     
BUFFER_SIZE = 4096         
VREF = 3.3              
MAG_MIN_THRESHOLD = 3000   
MIN_FREQ = 175
LARG_CANAL = 50

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

    print("Coletando sinal para deteccao de frequencia...")

    while indice < BUFFER_SIZE:
        inicio_loop = time.perf_counter()
        buffer[indice] = ler_tensao_protegida()
        indice += 1
        #time.sleep(1 / SAMPLING_RATE)
        tempo_decorrido = time.perf_counter() - inicio_loop
        if tempo_decorrido < (1 / SAMPLING_RATE):
            time.sleep((1 / SAMPLING_RATE) - tempo_decorrido)

    sinal_normalizado = normalizar_sinal(buffer)

    n = len(sinal_normalizado)
    yf = rfft(sinal_normalizado)
    xf = rfftfreq(n, 1 / SAMPLING_RATE)
    magnitudes = np.abs(yf)
    magnitudes[0] = 0 

    # indices_validos = np.where(xf >= 200)[0]
    # if len(indices_validos) == 0:
    #    return 0
    
    # Considera somente frequencias acima de 200 Hz e magnitudes acima do limiar
    indices_validos = np.where(xf >= 200)[0]
    indices_validos2 = np.where(magnitudes >= MAG_MIN_THRESHOLD)[0]
    indices_validos = np.intersect1d(indices_validos, indices_validos2)
    if len(indices_validos) == 0:
        return 0

    # Calcula a frequencia dominante
    idx_max = indices_validos[np.argmax(magnitudes[indices_validos])]
    freq = xf[idx_max]

    # Calcula o canal correspondente
    # min_freq = 175
    # larg_canal = 50
    # b = (freq_dominante - min_freq) // larg_canal
    # canal_freq = int(min_freq + larg_canal / 2 + b * larg_canal)
    b = (freq - MIN_FREQ) // LARG_CANAL
    canal = max(0,int(MIN_FREQ + LARG_CANAL / 2 + b * LARG_CANAL))
    if canal < MIN_FREQ:
        canal = 0

    return canal

import atexit
@atexit.register
def cleanup():
    spi.close()
    print("\nSPI finalizado.")