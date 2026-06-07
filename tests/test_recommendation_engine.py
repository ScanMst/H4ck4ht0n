from recommendation_engine import generar_oportunidades

contexto = {
    "cliente_alias": "Fernanda",
    "cedis": "MTY01",
    "meta": "Aumentar ventas e incrementar ticket promedio",

    "historial_compras": [
        {"compra": 1, "fecha": "2026-01-01", "productos": ["Coca-Cola"]},
        {"compra": 2, "fecha": "2026-01-08", "productos": ["Coca-Cola", "Sprite"]},
        {"compra": 3, "fecha": "2026-01-15", "productos": ["Coca-Cola"]},
        {"compra": 4, "fecha": "2026-01-22", "productos": ["Sprite"]},
        {"compra": 5, "fecha": "2026-01-29", "productos": ["Sprite"]},
        {"compra": 6, "fecha": "2026-03-01", "productos": ["Coca-Cola"]},
        {"compra": 7, "fecha": "2026-03-08", "productos": ["Coca-Cola", "Sprite"]},
        {"compra": 8, "fecha": "2026-03-15", "productos": ["Sprite"]},
        {"compra": 9, "fecha": "2026-03-22", "productos": ["Sprite"]},
        {"compra": 10, "fecha": "2026-03-29", "productos": ["Coca-Cola"]}
    ],

    "ultima_compra": {
        "fecha": "2026-03-29",
        "productos": ["Coca-Cola"],
        "dias_desde_ultima_compra": 29
    },

    "productos_oportunidad_cedis": [
        {
            "producto": "Powerade Moras",
            "score": 88,
            "evidencia": "Powerade tiene alta rotación en negocios similares del CEDIS MTY01."
        }
    ],

    "promociones_disponibles": [
        {"producto": "Sabritas", "promo": "15% de descuento"}
    ],

    "loyalty": {
        "puntos_actuales": 340,
        "regla": "$20 MXN en compras = 1 punto"
    },

    "pedido_sugerido": ["Coca-Cola", "Sprite", "Powerade Moras", "Sabritas"]
}

resultado = generar_oportunidades(contexto)

print(resultado)