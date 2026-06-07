from recommendation_engine import generar_oportunidades
from growth_agent import generar_recomendacion

contexto_cliente = {
    "cliente": "Fernanda",
    "tipo_cliente": "Madre emprendedora",
    "meta": "Aumentar ventas e incrementar ticket promedio",

    "resumen_comportamiento": {
        "total_compras": 10,
        "periodo_analizado": "enero a abril 2026",
        "dias_desde_ultima_compra": 29,
        "producto_mas_frecuente": "Coca-Cola",
        "veces_coca_cola": 6,
        "veces_sprite": 5,
        "combo_coca_sprite": 2,
        "patron_detectado": "El cliente alterna entre Coca-Cola y Sprite. Coca-Cola aparece ligeramente más frecuente.",
        "tipo_comportamiento": "Cliente recurrente con preferencia por productos conocidos"
    },

"productos_oportunidad_cedis": [
    {
        "producto": "Powerade",
        "score": 88,
        "evidencia": "Powerade tiene alta rotación en negocios similares del CEDIS MTY01."
    }
],

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

    "productos_frecuentes": [
        {"producto": "Coca-Cola", "veces_comprado": 6, "ultima_compra": "2026-03-29"},
        {"producto": "Sprite", "veces_comprado": 5, "ultima_compra": "2026-03-22"}
    ],

    "productos_comprados_una_o_dos_veces": [
        {"producto": "Powerade", "veces_comprado": 1, "comentario": "Producto probado una vez, no recurrente todavía"}
    ],

    "productos_oportunidad_cedis": [
        {"producto": "Powerade", "motivo": "Alta rotación en negocios similares"},
        {"producto": "Sabritas", "motivo": "Alta demanda en la zona"}
    ],

    "promociones_disponibles": [
        {"producto": "Sabritas", "promo": "15% de descuento"},
        {"producto": "Coca-Cola", "promo": "Puntos extra en Loyalty"}
    ],

    "loyalty": {
        "puntos_actuales": 340,
        "regla": "$20 MXN en compras = 1 punto",
        "beneficio": "Puede acumular puntos adicionales cumpliendo retos personalizados"
    },

    "pedido_sugerido": [
        "Coca-Cola",
        "Sprite",
        "Powerade",
        "Sabritas"
    ]
}

oportunidades = generar_oportunidades(contexto_cliente)
resultado = generar_recomendacion(oportunidades)
print(resultado)