import spidev
import time
import numpy as np
from scipy.fft import rfft, rfftfreq

SAMPLING_RATE = 2000  
BUFFER_SIZE = 4000    
VREF = 3.3           

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

def ler_tensao_protegida():
    dados = spi.xfer2([0x00, 0x00])
    valor = ((dados[0] & 0x1F) << 7) | (dados[1] >> 1)
    return min(valor, 4095)

def calcular_frequencia(sinal, taxa_amostragem):
    n = len(sinal)
    yf = rfft(sinal)
    xf = rfftfreq(n, 1/taxa_amostragem)
    idx = np.argmax(np.abs(yf[1:])) + 1 
    freq = xf[idx]
    return freq if freq > 200 else 0  

def normalizar_sinal(sinal):
    media = np.mean(sinal)
    return sinal - media

try:
    print("Iniciando detector de frequencia...")
    print("Certifique-se que a fonte de luz esta piscando em uma frequencia constante")
    
    buffer = np.zeros(BUFFER_SIZE)
    indice = 0
    
    print("\nAguardando dados...")
    
    while True:
        inicio_loop = time.perf_counter()
        
        buffer[indice] = ler_tensao_protegida()
        indice += 1
        
        if indice >= BUFFER_SIZE:
            sinal_normalizado = normalizar_sinal(buffer)
            freq = calcular_frequencia(sinal_normalizado, SAMPLING_RATE)
            tensao_media = (np.mean(buffer)/4095)*VREF
            amp = np.max(sinal_normalizado)
            
            print(f"Freq: {freq:.2f} Hz | Vmed: {tensao_media:.2f}V | Amp: {amp:.0f}", end='\r')
            
            indice = 0 
        
        tempo_decorrido = time.perf_counter() - inicio_loop
        if tempo_decorrido < (1/SAMPLING_RATE):
            time.sleep((1/SAMPLING_RATE) - tempo_decorrido)

except KeyboardInterrupt:
    print("\nDetecção encerrada")

finally:
    spi.close()
    print("Recursos liberados")
