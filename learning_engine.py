from datetime import datetime
from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]


def calcular_aprendizaje():
    feedbacks = list(db.feedback.find({}))

    resumen = {}

    for fb in feedbacks:
        producto = fb.get("producto")
        tipo = fb.get("tipo_recomendacion")
        respuesta = fb.get("respuesta")

        clave = f"{producto}|{tipo}"

        if clave not in resumen:
            resumen[clave] = {
                "producto": producto,
                "tipo_recomendacion": tipo,
                "total_feedback": 0,
                "aceptadas": 0,
                "rechazadas": 0,
                "tasa_aceptacion": 0,
                "aprendizaje": ""
            }

        resumen[clave]["total_feedback"] += 1

        if respuesta == "agregar":
            resumen[clave]["aceptadas"] += 1
        elif respuesta == "no_me_interesa":
            resumen[clave]["rechazadas"] += 1

    docs = []

    for item in resumen.values():
        total = item["total_feedback"]
        aceptadas = item["aceptadas"]

        tasa = round((aceptadas / total) * 100, 2) if total > 0 else 0

        item["tasa_aceptacion"] = tasa

        if tasa >= 70:
            item["aprendizaje"] = "Alta aceptación. Conviene seguir recomendando este producto."
        elif tasa >= 40:
            item["aprendizaje"] = "Aceptación media. Conviene recomendarlo solo con promociones o bajo riesgo."
        else:
            item["aprendizaje"] = "Baja aceptación. Conviene reducir prioridad en futuras recomendaciones."

        item["timestamp"] = datetime.now().isoformat()
        docs.append(item)

    db.learning_summary.delete_many({})

    if docs:
        db.learning_summary.insert_many(docs)

    print(f"Learning actualizado: {len(docs)} registros")
    return docs