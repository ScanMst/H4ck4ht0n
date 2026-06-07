from behavior_engine import analizar_comportamiento
from growth_agent import generar_recomendacion

compras = [
    {"orden": 1, "fecha": "2026-01-01", "productos": ["X"]},
    {"orden": 2, "fecha": "2026-01-07", "productos": ["X", "Y"]},
    {"orden": 3, "fecha": "2026-01-13", "productos": ["X"]},
    {"orden": 4, "fecha": "2026-01-20", "productos": ["Y"]},
    {"orden": 5, "fecha": "2026-01-28", "productos": ["Y"]},
    {"orden": 6, "fecha": "2026-03-02", "productos": ["X"]},
    {"orden": 7, "fecha": "2026-03-10", "productos": ["X", "Y"]},
    {"orden": 8, "fecha": "2026-03-17", "productos": ["Y"]},
    {"orden": 9, "fecha": "2026-03-25", "productos": ["Y"]},
    {"orden": 10, "fecha": "2026-04-01", "productos": ["X"]}
]

analisis = analizar_comportamiento(compras)

contexto = {
    "cliente": "Cliente ejemplo",
    "meta": "Aumentar ventas e incrementar ticket promedio",
    "analisis_comportamiento": analisis,
    "promociones": [
        "Combo X + Y con descuento",
        "Compra X y suma puntos extra",
        "Y participa en reto Loyalty"
    ],
    "loyalty": "Cada $20 MXN en compras suma 1 punto. Los retos personalizados dan puntos adicionales.",
    "pedido_sugerido": ["X", "Y"],
    "contexto_tuali": "El cliente puede recibir recomendaciones basadas en historial, promociones, loyalty y pedido sugerido."
}

print(generar_recomendacion(contexto))