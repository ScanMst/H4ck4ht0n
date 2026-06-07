import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")


PEDIDOS_COLUMNS = [
    "cliente_id",
    "pedido_id",
    "pais",
    "categoria",
    "cedis",
    "fecha_pedido",
    "estado_pedido",
    "metrica_1",
    "metrica_2",
    "metrica_3",
    "sku_id",
    "producto_id",
    "producto",
    "cantidad",
    "estado_producto"
]

METRICAS_COLUMNS = [
    "cliente_id",
    "pais",
    "categoria",
    "cedis",
    "producto_id",
    "producto",
    "num_pedidos",
    "cantidad_total",
    "frecuencia",
    "primera_compra",
    "ultima_compra",
    "dias_desde_ultima",
    "frecuencia_esperada",
    "flag_reabastecer",
    "ranking_cliente",
    "favorito"
]

POPULARIDAD_COLUMNS = [
    "cedis",
    "pais",
    "producto_id",
    "producto",
    "clientes_compradores",
    "cantidad_promedio",
    "ranking_popularidad"
]

TENDENCIAS_COLUMNS = [
    "cliente_id",
    "pais",
    "cedis",
    "producto_id",
    "producto",
    "clientes_similares",
    "venta_estimada",
    "ranking_cedis",
    "ranking_recomendacion"
]


def read_csv_no_header(filename, columns):
    path = DATA_DIR / filename

    try:
        df = pd.read_csv(
            path,
            header=None,
            names=columns,
            encoding="utf-8",
            low_memory=False
        )
    except UnicodeDecodeError:
        df = pd.read_csv(
            path,
            header=None,
            names=columns,
            encoding="latin1",
            low_memory=False
        )

    return df


def cargar_pedidos():
    df = read_csv_no_header("PEDIDOS_MAESTRA.csv", PEDIDOS_COLUMNS)
    df["fecha_pedido"] = pd.to_datetime(df["fecha_pedido"], errors="coerce")
    df["producto"] = df["producto"].astype(str).str.strip()
    return df


def cargar_metricas_cliente_producto():
    df = read_csv_no_header("TB_METRICAS_CLIENTE_PRODUCTO.csv", METRICAS_COLUMNS)
    df["primera_compra"] = pd.to_datetime(df["primera_compra"], errors="coerce")
    df["ultima_compra"] = pd.to_datetime(df["ultima_compra"], errors="coerce")
    df["producto"] = df["producto"].astype(str).str.strip()
    return df


def cargar_popularidad_producto():
    df = read_csv_no_header("TB_POPULARIDAD_PRODUCTO.csv", POPULARIDAD_COLUMNS)
    df["producto"] = df["producto"].astype(str).str.strip()
    return df


def cargar_recomendaciones_tendencia():
    df = read_csv_no_header("TB_RECOMENDACIONES_TENDENCIA.csv", TENDENCIAS_COLUMNS)
    df["producto"] = df["producto"].astype(str).str.strip()
    return df


def cargar_todo():
    return {
        "pedidos": cargar_pedidos(),
        "metricas": cargar_metricas_cliente_producto(),
        "popularidad": cargar_popularidad_producto(),
        "tendencias": cargar_recomendaciones_tendencia()
    }


if __name__ == "__main__":
    data = cargar_todo()

    for nombre, df in data.items():
        print("\n" + "=" * 80)
        print(nombre.upper())
        print("Shape:", df.shape)
        print(df.head())