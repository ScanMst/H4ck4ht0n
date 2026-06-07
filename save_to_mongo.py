from pymongo import MongoClient
from config import MONGO_URI, DB_NAME
from recommendation_engine import generar_oportunidades

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def guardar_recomendaciones_tableau(contexto_cliente):
    oportunidades = generar_oportunidades(contexto_cliente)

    docs = []

    for r in oportunidades["recomendaciones"]:
        docs.append({
            "cliente_id": contexto_cliente.get("cliente_id", "518361"),
            "cliente_nombre": oportunidades.get("cliente_alias", "Fernanda"),
            "cedis": oportunidades.get("cedis"),
            "tipo": r["tipo"],
            "producto": r["producto"],
            "score": r["score"],
            "titulo": f"{r['tipo'].replace('_', ' ').title()} - {r['producto']}",
            "evidencia": r["evidencia"],
            "motivo": r["motivo"],
            "prediccion": r["prediccion"],
            "impacto": r["impacto"],
            "accion": r["accion"],
            "boton_1": "Agregar",
            "boton_2": "No me interesa",
            "feedback": None,
            "timestamp": oportunidades["timestamp"]
        })

    db.tableau_recommendations.delete_many({
        "cliente_id": contexto_cliente.get("cliente_id", "518361")
    })

    if docs:
        db.tableau_recommendations.insert_many(docs)

    print(f"Guardadas {len(docs)} recomendaciones en MongoDB")


contexto = {
    "cliente_id": "518361",
    "cliente_alias": "Fernanda",
    "cedis": "MTY01",
    "meta": "Aumentar ventas e incrementar ticket promedio",

    "historial_compras": [
        {"fecha": "2026-01-01", "productos": ["Coca-Cola"]},
        {"fecha": "2026-01-08", "productos": ["Coca-Cola", "Sprite"]},
        {"fecha": "2026-01-15", "productos": ["Coca-Cola"]},
        {"fecha": "2026-03-29", "productos": ["Coca-Cola"]}
    ],

    "ultima_compra": {
        "fecha": "2026-03-29",
        "dias_desde_ultima_compra": 36
    },

    "productos_oportunidad_cedis": [
        {
            "producto": "Powerade Moras",
            "score": 88,
            "evidencia": "Lo compran negocios similares dentro de tu CEDIS."
        }
    ],

    "promociones_disponibles": [
        {"producto": "Sabritas", "promo": "15% de descuento"}
    ],

    "loyalty": {
        "puntos_actuales": 24138,
        "regla": "$20 MXN = 1 punto"
    },

    "pedido_sugerido": ["Coca-Cola", "Sprite", "Powerade Moras", "Sabritas"]
}

guardar_recomendaciones_tableau(contexto)