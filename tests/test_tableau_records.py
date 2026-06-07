from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

for doc in db.tableau_recommendations.find().limit(5):

    print("\n----------------")
    print("cliente_id:", doc.get("cliente_id"))
    print("cliente_alias:", doc.get("cliente_alias"))
    print("protopersona:", doc.get("protopersona"))
    print("producto:", doc.get("producto"))