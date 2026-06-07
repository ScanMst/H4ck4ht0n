from collections import Counter
from datetime import datetime
from score_adjuster import ajustar_score_por_aprendizaje


def calcular_score(valor, maximo):
    if maximo == 0:
        return 0
    return min(round((valor / maximo) * 100), 100)


def generar_oportunidades(contexto: dict) -> dict:
    compras = contexto.get("historial_compras", [])
    promociones = contexto.get("promociones_disponibles", [])
    productos_cedis = contexto.get("productos_oportunidad_cedis", [])
    loyalty = contexto.get("loyalty", {})
    pedido_sugerido = contexto.get("pedido_sugerido", [])
    productos_frecuentes = contexto.get("productos_frecuentes", [])

    recomendaciones = []
    contador = Counter()
    total_compras = len(compras)

    for compra in compras:
        contador.update(compra.get("productos", []))

    # ======================================================
    # 1. REABASTECIMIENTO
    # Prioridad 1: historial de compras
    # Prioridad 2: productos_frecuentes desde métricas
    # ======================================================

    if contador:
        producto_reabastecimiento, veces_producto = contador.most_common(1)[0]

        dias_sin_comprar = contexto.get("ultima_compra", {}).get(
            "dias_desde_ultima_compra",
            0
        )

        score_base = min(
            calcular_score(veces_producto, max(total_compras, 1)) + min(dias_sin_comprar, 30),
            100
        )

        evidencia = (
            f"Has comprado {producto_reabastecimiento} {veces_producto} veces "
            f"en tus últimas {total_compras} compras y han pasado "
            f"{dias_sin_comprar} días desde tu último pedido."
        )

    elif productos_frecuentes:
        producto_info = productos_frecuentes[0]
        producto_reabastecimiento = producto_info.get("producto")
        veces_producto = producto_info.get("veces_comprado", 1)
        ranking = producto_info.get("ranking_cliente", "N/D")
        ultima_compra = producto_info.get("ultima_compra", "N/D")

        try:
            veces_num = int(veces_producto)
        except Exception:
            veces_num = 1

        score_base = min(70 + max(0, 10 - int(ranking)) if str(ranking).isdigit() else 75, 100)

        evidencia = (
            f"{producto_reabastecimiento} aparece dentro de tus productos frecuentes "
            f"con ranking #{ranking}. Última compra registrada: {ultima_compra}."
        )

    else:
        producto_reabastecimiento = None

    if producto_reabastecimiento:
        score_reabastecimiento, motivo_aprendizaje = ajustar_score_por_aprendizaje(
            producto_reabastecimiento,
            "reabastecimiento",
            score_base
        )

        recomendaciones.append({
            "tipo": "reabastecimiento",
            "producto": producto_reabastecimiento,
            "score": score_reabastecimiento,
            "evidencia": evidencia,
            "motivo": "Es uno de tus productos con mayor necesidad de reposición según tu historial.",
            "prediccion": "Alta" if score_reabastecimiento >= 75 else "Media",
            "accion": f"Agregar {producto_reabastecimiento} a tu pedido sugerido.",
            "impacto": "Evitar quedarte sin inventario de un producto recurrente.",
            "motivo_aprendizaje": motivo_aprendizaje
        })

    # ======================================================
    # 2. OPORTUNIDAD CEDIS / TENDENCIA
    # ======================================================

    if productos_cedis:
        producto_cedis = productos_cedis[0]
        score_original = producto_cedis.get("score", 80)

        score_cedis, motivo_aprendizaje_cedis = ajustar_score_por_aprendizaje(
            producto_cedis["producto"],
            "oportunidad_cedis",
            score_original
        )

        recomendaciones.append({
            "tipo": "oportunidad_cedis",
            "producto": producto_cedis["producto"],
            "score": score_cedis,
            "evidencia": producto_cedis.get(
                "evidencia",
                "Este producto tiene buena rotación en negocios similares de tu zona."
            ),
            "motivo": "Puede ayudarte a probar demanda sin arriesgar demasiado.",
            "motivo_aprendizaje": motivo_aprendizaje_cedis,
            "prediccion": "Alta" if score_cedis >= 90 else "Media",
            "accion": f"Agregar pocas unidades de {producto_cedis['producto']} para prueba.",
            "impacto": "Aumentar variedad en tu tienda con bajo riesgo."
        })

    # ======================================================
    # 3. PROMOCIÓN
    # ======================================================

    if promociones:
        promo = promociones[0]
        score_original = promo.get("score", 85)

        score_promo, motivo_aprendizaje_promo = ajustar_score_por_aprendizaje(
            promo["producto"],
            "promocion",
            score_original
        )

        recomendaciones.append({
            "tipo": "promocion",
            "producto": promo["producto"],
            "score": score_promo,
            "evidencia": f"{promo['producto']} tiene promoción: {promo['promo']}.",
            "motivo": "La promoción puede ayudarte a incrementar el valor del pedido.",
            "motivo_aprendizaje": motivo_aprendizaje_promo,
            "prediccion": "Alta" if score_promo >= 80 else "Media",
            "accion": f"Agregar {promo['producto']} aprovechando la promoción.",
            "impacto": "Incrementar ticket promedio con una compra incentivada."
        })

    productos_validos = set(pedido_sugerido)

    for r in recomendaciones:
        productos_validos.add(r["producto"])

    return {
        "cliente_alias": contexto.get("cliente_alias", "Cliente"),
        "cliente_id": contexto.get("cliente_id"),
        "cliente_id": contexto.get("cliente_id"),
        "protopersona": contexto.get("protopersona", "madre_emprendedora"),
        "meta": contexto.get("meta"),
        "cedis": contexto.get("cedis"),
        "total_compras": total_compras,
        "producto_reabastecimiento": recomendaciones[0]["producto"] if recomendaciones else None,
        "frecuencia_productos": dict(contador),
        "recomendaciones": recomendaciones,
        "loyalty": loyalty,
        "pedido_sugerido": pedido_sugerido,
        "productos_validos": list(productos_validos),
        "timestamp": datetime.now().isoformat()
    }