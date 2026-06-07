from growth_agent import generar_recomendacion

contexto = {
    "cliente": "Fernanda",
    "meta": "Aumentar ventas",
    "ultima_compra": {
        "fecha": "2026-06-01",
        "monto": 850,
        "productos": ["Coca-Cola 600ml", "Sprite 600ml"]
    },
    "productos_frecuentes": ["Coca-Cola 600ml", "Sprite 600ml"],
    "productos_comprados_una_vez": ["Powerade", "Topo Chico"],
    "productos_populares_zona": ["Powerade", "Coca-Cola 2L", "Fanta"],
    "promociones": ["Powerade 12 pack", "Coca-Cola 2L con descuento"],
    "loyalty": "Le faltan 250 puntos para una recompensa",
    "pedido_sugerido": ["Coca-Cola 600ml", "Powerade"]
}

print(generar_recomendacion(contexto))