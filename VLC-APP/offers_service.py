from firebase_connector import FirebaseConnector
from typing import List, Dict

class OffersService:
    def __init__(self):
        self.db = FirebaseConnector()

    def get_hotspot_products(self, hotspot_id: str) -> List[Dict]:
        offers_ref = self.db.collection('ofertas')

        try:
            query = offers_ref.where('hotspotId', '==', hotspot_id).stream()
            return [self._process_offer(doc) for doc in query]
        except Exception as e:
            print(f"Erro ao consultar ofertas: {str(e)}")
            return []

    def _process_offer(self, doc) -> Dict:
        offer = doc.to_dict()
        offer['id'] = doc.id
        return offer
