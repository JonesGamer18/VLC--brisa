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

