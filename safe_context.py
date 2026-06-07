def build_safe_context(cliente_contexto: dict) -> dict:
    """
    Solo manda al LLM datos resumidos.
    No manda CSV completo, teléfonos, direcciones ni datos sensibles.
    """

    return {
        "cliente_alias": cliente_contexto.get("cliente_alias", "Cliente"),
        "tipo_cliente": cliente_contexto.get("tipo_cliente"),
        "meta": cliente_contexto.get("meta"),
        "cedis": cliente_contexto.get("cedis"),
        "resumen_comportamiento": cliente_contexto.get("resumen_comportamiento"),
        "productos_frecuentes": cliente_contexto.get("productos_frecuentes"),
        "productos_oportunidad_cedis": cliente_contexto.get("productos_oportunidad_cedis"),
        "promociones_disponibles": cliente_contexto.get("promociones_disponibles"),
        "loyalty": cliente_contexto.get("loyalty"),
        "pedido_sugerido": cliente_contexto.get("pedido_sugerido"),
    }