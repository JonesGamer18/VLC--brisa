import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path
import json
import os

class FirebaseConnector:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            try:
                current_dir = Path(__file__).parent
                config_path = current_dir / 'firebase_config.json'
                
                if not config_path.exists():
                    raise FileNotFoundError(
                        f"Arquivo firebase_config.json não encontrado em: {config_path}\n"
                        f"Diretório atual: {current_dir}\n"
                        f"Conteúdo do diretório: {os.listdir(current_dir)}"
                    )
                
                with open(config_path) as f:
                    config = json.load(f)
                
                cred = credentials.Certificate({
                    "type": config["type"],
                    "project_id": config["project_id"],
                    "private_key_id": config["private_key_id"],
                    "private_key": config["private_key"].replace('\\n', '\n'),
                    "client_email": config["client_email"],
                    "client_id": config["client_id"],
                    "auth_uri": config["auth_uri"],
                    "token_uri": config["token_uri"],
                    "auth_provider_x509_cert_url": config["auth_provider_x509_cert_url"],
                    "client_x509_cert_url": config["client_x509_cert_url"]
                })
                
                firebase_admin.initialize_app(cred)
                cls._instance = firestore.client()
                
            except Exception as e:
                print("🔥 Erro ao configurar Firebase:")
                print(f"Tipo: {type(e).__name__}")
                print(f"Detalhes: {str(e)}")
                raise
                
        return cls._instance