from vlc_reader import detectar_frequencia
from offers_service import OffersService
from firebase_connector import FirebaseConnector
import firebase_admin
from firebase_admin import firestore
import time  

ID_CARRINHO_FIXO = "cr001"  

def encontrar_hotspot_por_frequencia(freq_detectada):
    db = FirebaseConnector()
    hotspots = db.collection('hotspots').stream()
    for doc in hotspots:
        data = doc.to_dict()
        if abs(data.get('frequency', 0) - freq_detectada) <= 5:
            return {
                "id": doc.id,
                "name": data.get("name", "sem_nome")
            }
    return None

def criar_ou_atualizar_carrinho(db, hotspot_id, ofertas):
    carrinhos_ref = db.collection("carrinhos")
    carrinho_doc = carrinhos_ref.document(ID_CARRINHO_FIXO)

    if not carrinho_doc.get().exists:
        print("Criando novo carrinho...")
        carrinho_doc.set({
            "localizacaoAtual": hotspot_id if hotspot_id else "desconhecido",
            "ofertasExibidas": ofertas,
            "tempoDeSessao": 12
        })
    else:
        print("Atualizando carrinho existente...")
        carrinho_doc.update({
            "localizacaoAtual": hotspot_id if hotspot_id else "desconhecido",
            "ofertasExibidas": ofertas,
            "tempoDeSessao": 12
        })

def enviar_frequencia_para_banco():
    freq = detectar_frequencia()
    print(f"\nFrequência detectada: {freq:.2f} Hz")

    hotspot_info = encontrar_hotspot_por_frequencia(freq)
    nome_hotspot = hotspot_info["name"] if hotspot_info else None
    hotspot_id = hotspot_info["id"] if hotspot_info else None

    ofertas_titulos = []
    if hotspot_id:
        print(f"Hotspot correspondente: ({hotspot_id})")
        svc = OffersService()
        produtos = svc.get_hotspot_products(hotspot_id)
        ofertas_titulos = [p.get("title", "sem_titulo") for p in produtos]
    else:
        print("Nenhum hotspot correspondente encontrado.")

    db = FirebaseConnector()
    criar_ou_atualizar_carrinho(db, hotspot_id, ofertas_titulos)

if __name__ == "__main__":
    print("Sistema iniciado. Pressione Ctrl+C para encerrar.")
    try:
        while True:
            enviar_frequencia_para_banco()
            time.sleep(5) 
    except KeyboardInterrupt:
        print("\nSistema encerrado pelo usuário.")
