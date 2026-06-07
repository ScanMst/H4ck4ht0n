from pymongo import MongoClient
from config import MONGO_URI, DB_NAME
from build_context_from_csv import build_context
from recommendation_engine import generar_oportunidades
from growth_agent import generar_recomendacion

client = MongoClient(MONGO_URI)
db = client[DB_NAME]


def guardar_para_tableau(cliente_id):
    contexto = build_context(cliente_id)
    oportunidades = generar_oportunidades(contexto)

    print(f"Recomendaciones generadas: {len(oportunidades.get('recomendaciones', []))}")

    respuesta_agente = generar_recomendacion(oportunidades)

    docs = []

    for r in oportunidades.get("recomendaciones", []):
        docs.append({
            "cliente_id": contexto.get("cliente_id"),
            "cliente_alias": contexto.get("cliente_alias"),
            "protopersona": contexto.get("protopersona"),
            "pais": contexto.get("pais"),
            "cedis": contexto.get("cedis"),
            "meta": contexto.get("meta"),

            "tipo": r.get("tipo"),
            "producto": r.get("producto"),
            "score": r.get("score"),
            "titulo": f"{r.get('tipo', '').replace('_', ' ').title()} - {r.get('producto')}",
            "evidencia": r.get("evidencia"),
            "motivo": r.get("motivo"),
            "prediccion": r.get("prediccion"),
            "impacto": r.get("impacto"),
            "accion": r.get("accion"),
            "motivo_aprendizaje": r.get("motivo_aprendizaje", "Sin aprendizaje previo"),

            "boton_1": "Agregar",
            "boton_2": "No me interesa",
            "feedback": None,

            "texto_agente": respuesta_agente,
            "timestamp": oportunidades.get("timestamp")
        })

    db.tableau_recommendations.delete_many({
        "cliente_id": contexto.get("cliente_id")
    })

    if docs:
        db.tableau_recommendations.insert_many(docs)

    db.agent_outputs.insert_one({
        "cliente_id": contexto.get("cliente_id"),
        "cliente_alias": contexto.get("cliente_alias"),
        "protopersona": contexto.get("protopersona"),
        "cedis": contexto.get("cedis"),
        "respuesta_agente": respuesta_agente,
        "timestamp": oportunidades.get("timestamp")
    })

    print(f"Cliente: {contexto.get('cliente_id')}")
    print(f"Alias: {contexto.get('cliente_alias')}")
    print(f"Protopersona: {contexto.get('protopersona')}")
    print(f"CEDIS: {contexto.get('cedis')}")
    print(f"Recomendaciones guardadas: {len(docs)}")
    print("\nRESPUESTA DEL AGENTE:\n")
    print(respuesta_agente)


if __name__ == "__main__":
    # Limpieza opcional para dejar Tableau con datos frescos de demo
    db.tableau_recommendations.delete_many({})
    db.agent_outputs.delete_many({})

    clientes = [
        "1000040000000000000",
        "1021040000000000000",
        "1021100000000000000"
    ]

    for cliente in clientes:
        print("\n" + "=" * 80)
        print("CLIENTE:", cliente)
        print("=" * 80)
        guardar_para_tableau(cliente)