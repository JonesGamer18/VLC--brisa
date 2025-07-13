<<<<<<< HEAD
from firebase_connector import FirebaseConnector
from typing import Dict, Any, Optional

class HotspotsService:
    def __init__(self):
        self.db = FirebaseConnector()
    
    def get_all_hotspots(self) -> Dict[str, Dict[str, Any]]:
        docs = self.db.collection('hotspots').stream()
        return {doc.id: doc.to_dict() for doc in docs}
    
    def get_hotspot_by_id(self, hotspot_id: str) -> Optional[Dict[str, Any]]:
        doc = self.db.collection('hotspots').document(hotspot_id).get()
        return doc.to_dict() if doc.exists else None
    
    def get_hotspot_by_frequency(self, frequency: float, tolerance: int = 5) -> Optional[Dict[str, Any]]:
        hotspots = self.get_all_hotspots()
        for hotspot_id, data in hotspots.items():
            if 'frequency' in data and abs(data['frequency'] - frequency) <= tolerance:
                return {'id': hotspot_id, **data}
        return None
=======
from firebase_connector import FirebaseConnector #importar firebase
from google.cloud import firestore

class HotspotService:
    def __init__(self):
        self.db = FirebaseConnector() #herança de atributos/metodos

    def get_all_hotspots(self):
        doc = self.db.collection('hotspots').stream() 
        return (doc.id:doc.to_dict() for doc in docs)

    def get_hotspot_by_id(self, hotspot_id):
        doc = self.db.collection('hotspots').document(hotspot_id).get()
        return doc.to_dict() if doc.exists else None
    
 #   def get_nearby_hotspots(self, x, y, radius=5):
 #       hotspots = self.get_all_hotspots()
 #       nearby = []

>>>>>>> eeba3a36b27823c811468b188048243863a81521
