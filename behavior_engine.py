from collections import Counter

def analizar_comportamiento(compras):
    total_compras = len(compras)

    contador_productos = Counter()
    combinaciones = Counter()

    for compra in compras:
        productos = compra["productos"]
        contador_productos.update(productos)

        if len(productos) > 1:
            combinaciones.update([" + ".join(sorted(productos))])

    productos_frecuentes = contador_productos.most_common()

    ultima_compra = compras[-1]
    productos_ultima_compra = ultima_compra["productos"]

    prediccion = productos_frecuentes[0][0] if productos_frecuentes else None

    return {
        "total_compras": total_compras,
        "frecuencia_productos": dict(productos_frecuentes),
        "combinaciones": dict(combinaciones),
        "ultima_compra": ultima_compra,
        "producto_mas_probable": prediccion,
        "productos_ultima_compra": productos_ultima_compra
    }