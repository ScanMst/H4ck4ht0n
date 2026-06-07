import pandas as pd
from datetime import datetime
from data_loader import (
    cargar_pedidos,
    cargar_metricas_cliente_producto,
    cargar_popularidad_producto,
    cargar_recomendaciones_tendencia
)


def suma_columna_segura(df, columnas_posibles):
    for col in columnas_posibles:
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce").fillna(0).sum()
    return 0


def build_context(cliente_id):
    pedidos = cargar_pedidos()
    metricas = cargar_metricas_cliente_producto()
    popularidad = cargar_popularidad_producto()
    tendencias = cargar_recomendaciones_tendencia()

    cliente_id = str(cliente_id)

    pedidos_cliente = pedidos[pedidos["cliente_id"].astype(str) == cliente_id].copy()
    metricas_cliente = metricas[metricas["cliente_id"].astype(str) == cliente_id].copy()
    tendencias_cliente = tendencias[tendencias["cliente_id"].astype(str) == cliente_id].copy()

    if pedidos_cliente.empty and metricas_cliente.empty and tendencias_cliente.empty:
        raise ValueError(f"No encontré datos para cliente_id: {cliente_id}")

    protopersonas = {
        "1000040000000000000": "madre_emprendedora",
        "1021040000000000000": "dueno_apoyado",
        "1021100000000000000": "familiar_comprometida"
    }

    protopersona = protopersonas.get(cliente_id, "madre_emprendedora")

    nombres_demo = {
        "madre_emprendedora": "Fernanda",
        "dueno_apoyado": "Raúl",
        "familiar_comprometida": "Fernanda"
    }

    cliente_alias = nombres_demo.get(protopersona, f"Cliente {cliente_id[-4:]}")

    if not metricas_cliente.empty:
        cedis = metricas_cliente.iloc[0].get("cedis")
        pais = metricas_cliente.iloc[0].get("pais")
    elif not tendencias_cliente.empty:
        cedis = tendencias_cliente.iloc[0].get("cedis")
        pais = tendencias_cliente.iloc[0].get("pais")
    else:
        cedis = pedidos_cliente.iloc[0].get("cedis")
        pais = pedidos_cliente.iloc[0].get("pais")

    historial_compras = []
    productos_ultima = []
    ultima_fecha = None
    dias_desde_ultima = 0

    if not pedidos_cliente.empty:
        pedidos_cliente["fecha_pedido"] = pd.to_datetime(
            pedidos_cliente["fecha_pedido"],
            errors="coerce"
        )

        pedidos_cliente = pedidos_cliente.dropna(subset=["fecha_pedido"])
        pedidos_cliente = pedidos_cliente.sort_values("fecha_pedido")

        if not pedidos_cliente.empty:
            ultima_fecha = pedidos_cliente["fecha_pedido"].max()
            dias_desde_ultima = (datetime.now() - ultima_fecha.to_pydatetime()).days

            productos_ultima = (
                pedidos_cliente[pedidos_cliente["fecha_pedido"] == ultima_fecha]["producto"]
                .dropna()
                .astype(str)
                .str.strip()
                .unique()
                .tolist()
            )

            for fecha, grupo in pedidos_cliente.groupby("fecha_pedido"):
                productos = (
                    grupo["producto"]
                    .dropna()
                    .astype(str)
                    .str.strip()
                    .unique()
                    .tolist()
                )

                historial_compras.append({
                    "fecha": str(fecha.date()),
                    "productos": productos
                })

    productos_frecuentes = []

    if not metricas_cliente.empty:
        metricas_cliente["ranking_cliente_num"] = pd.to_numeric(
            metricas_cliente.get("ranking_cliente", 999),
            errors="coerce"
        ).fillna(999)

        favoritos = metricas_cliente.sort_values("ranking_cliente_num").head(5)

        for _, row in favoritos.iterrows():
            productos_frecuentes.append({
                "producto": str(row.get("producto", "")).strip(),
                "veces_comprado": row.get("num_pedidos", 1),
                "ranking_cliente": row.get("ranking_cliente", "N/D"),
                "ultima_compra": str(row.get("ultima_compra", "N/D"))
            })

    productos_oportunidad_cedis = []

    if not tendencias_cliente.empty:
        tendencias_cliente["ranking_recomendacion_num"] = pd.to_numeric(
            tendencias_cliente.get("ranking_recomendacion", 999),
            errors="coerce"
        ).fillna(999)

        top_tendencias = tendencias_cliente.sort_values("ranking_recomendacion_num").head(3)

        for _, row in top_tendencias.iterrows():
            productos_oportunidad_cedis.append({
                "producto": str(row.get("producto", "")).strip(),
                "score": 85,
                "evidencia": (
                    f"{row.get('producto')} aparece como recomendación "
                    f"#{row.get('ranking_recomendacion')} para negocios similares de tu CEDIS. "
                    f"Lo compran {row.get('clientes_similares')} clientes similares."
                )
            })

    if not productos_oportunidad_cedis:
        pop_cedis = popularidad[
            popularidad["cedis"].astype(str) == str(cedis)
        ].copy()

        if not pop_cedis.empty:
            pop_cedis["ranking_popularidad_num"] = pd.to_numeric(
                pop_cedis.get("ranking_popularidad", 999),
                errors="coerce"
            ).fillna(999)

            pop_cedis = pop_cedis.sort_values("ranking_popularidad_num").head(3)

            for _, row in pop_cedis.iterrows():
                productos_oportunidad_cedis.append({
                    "producto": str(row.get("producto", "")).strip(),
                    "score": 75,
                    "evidencia": (
                        f"{row.get('producto')} es popular en tu CEDIS "
                        f"con ranking #{row.get('ranking_popularidad')}."
                    )
                })

    promociones = []

    productos_promo = popularidad[
        popularidad["producto"].astype(str).str.contains("Promo", case=False, na=False)
    ].head(3)

    for _, row in productos_promo.iterrows():
        promociones.append({
            "producto": str(row.get("producto", "")).strip(),
            "promo": "Promoción disponible"
        })

    cantidad_pedidos = suma_columna_segura(
        pedidos_cliente,
        ["cantidad", "metrica_1", "metrica_2", "metrica_3"]
    )

    cantidad_metricas = suma_columna_segura(
        metricas_cliente,
        ["cantidad_total", "num_pedidos", "frecuencia"]
    )

    base_puntos = cantidad_pedidos if cantidad_pedidos > 0 else cantidad_metricas

    puntos_estimados = int(base_puntos)

    pedido_sugerido = list(set(
        [p["producto"] for p in productos_frecuentes if p.get("producto")] +
        [p["producto"] for p in productos_oportunidad_cedis if p.get("producto")]
    ))

    contexto = {
        "cliente_id": cliente_id,
        "cliente_alias": cliente_alias,
        "protopersona": protopersona,
        "pais": pais,
        "cedis": str(cedis),
        "meta": "Aumentar ventas e incrementar ticket promedio",

        "historial_compras": historial_compras[-20:],

        "ultima_compra": {
            "fecha": str(ultima_fecha),
            "productos": productos_ultima,
            "dias_desde_ultima_compra": dias_desde_ultima
        },

        "productos_frecuentes": productos_frecuentes,
        "productos_oportunidad_cedis": productos_oportunidad_cedis,
        "promociones_disponibles": promociones,

        "loyalty": {
            "puntos_actuales": puntos_estimados,
            "regla": "$20 MXN en compras = 1 punto",
            "beneficio": "Cumpliendo retos personalizados puedes obtener puntos adicionales."
        },

        "pedido_sugerido": pedido_sugerido
    }

    return contexto


if __name__ == "__main__":
    cliente = "1021040000000000000"
    contexto = build_context(cliente)

    print("Cliente ID:", contexto.get("cliente_id"))
    print("Cliente alias:", contexto.get("cliente_alias"))
    print("Protopersona:", contexto.get("protopersona"))
    print("CEDIS:", contexto.get("cedis"))
    print("Puntos:", contexto.get("loyalty", {}).get("puntos_actuales"))

    print("\nProductos frecuentes:")
    for p in contexto.get("productos_frecuentes", [])[:5]:
        print("-", p.get("producto"))

    print("\nOportunidades CEDIS:")
    for p in contexto.get("productos_oportunidad_cedis", [])[:3]:
        print("-", p.get("producto"))