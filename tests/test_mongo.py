from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")

    db = client[DB_NAME]
    print("MongoDB conectado correctamente")
    print("Base de datos:", DB_NAME)
    print("Colecciones:", db.list_collection_names())

except Exception as e:
    print("Error conectando a MongoDB:")
    print(e)