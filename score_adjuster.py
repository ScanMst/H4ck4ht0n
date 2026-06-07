from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]


def ajustar_score_por_aprendizaje(producto, tipo_recomendacion, score_original):
    learning = db.learning_summary.find_one({
        "producto": producto,
        "tipo_recomendacion": tipo_recomendacion
    })

    if not learning:
        return score_original, "Sin aprendizaje previo"

    tasa = learning.get("tasa_aceptacion", 0)

    if tasa >= 70:
        score_ajustado = min(score_original + 10, 100)
        motivo = "Score aumentado por alta aceptación histórica"
    elif tasa >= 40:
        score_ajustado = score_original
        motivo = "Score mantenido por aceptación media"
    else:
        score_ajustado = max(score_original - 15, 0)
        motivo = "Score reducido por baja aceptación histórica"

    return score_ajustado, motivo