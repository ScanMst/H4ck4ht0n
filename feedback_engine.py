from datetime import datetime
from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def guardar_feedback(cliente_id, producto, tipo_recomendacion, respuesta):
    doc = {
        "cliente_id": cliente_id,
        "producto": producto,
        "tipo_recomendacion": tipo_recomendacion,
        "respuesta": respuesta,  # agregar / no_me_interesa
        "timestamp": datetime.now().isoformat()
    }

    db.feedback.insert_one(doc)

    db.tableau_recommendations.update_one(
        {
            "cliente_id": cliente_id,
            "producto": producto,
            "tipo": tipo_recomendacion
        },
        {
            "$set": {
                "feedback": respuesta,
                "feedback_timestamp": doc["timestamp"]
            }
        }
    )

    print("Feedback guardado correctamente")