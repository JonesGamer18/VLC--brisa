from vlc_reader import detectar_frequencia
from offers_service import OffersService
from firebase_connector import FirebaseConnector
import time

def encontrar_hotspot_por_frequencia(freq_detectada):
    db = FirebaseConnector()
    hotspots = db.collection('hotspots').stream()
    for doc in hotspots:
        data = doc.to_dict()
        if abs(data.get('frequency', 0) - freq_detectada) <= 5:
            return doc.id
    return None

def mostrar_produtos_por_frequencia(freq):
    hotspot_id = encontrar_hotspot_por_frequencia(freq)
    if hotspot_id:
        print(f"\n Hotspot correspondente: {hotspot_id}")
        svc = OffersService()
        produtos = svc.get_hotspot_products(hotspot_id)

        print(f"\n PRODUTOS NO HOTSPOT {hotspot_id}")
        print("=" * 60)
        for prod in produtos:
            print(f"\n Nome:{prod.get('title', 'Sem nome')}")
            print(f"DescriÃ§Ã£o: {prod.get('description', '-')}")
        print(f"\n Total de produtos encontrados: {len(produtos)}\n")
    else:
        print(f"\n Nenhum hotspot encontrado para frequÃªncia {freq:.2f} Hz.")

def loop_principal():
    print("Iniciando sistema de recomendaÃ§Ã£o por VLC...\n")
    try:
        while True:
            freq = detectar_frequencia()
            print(f"\n? FrequÃªncia detectada: {freq:.2f} Hz")
            mostrar_produtos_por_frequencia(freq)
            time.sleep(10) 

    except KeyboardInterrupt:
        print("\n Encerrando sistema...")

if __name__ == "__main__":
    loop_principal()
