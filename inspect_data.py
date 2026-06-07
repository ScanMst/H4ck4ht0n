import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")

archivos = [
    "PEDIDOS_MAESTRA.csv",
    "TB_METRICAS_CLIENTE_PRODUCTO.csv",
    "TB_POPULARIDAD_PRODUCTO.csv",
    "TB_RECOMENDACIONES_TENDENCIA.csv"
]

for archivo in archivos:
    path = DATA_DIR / archivo

    print("\n" + "=" * 80)
    print(f"ARCHIVO: {archivo}")

    try:
        df = pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding="latin1")

    print("Shape:", df.shape)

    print("\nColumnas:")
    for i, col in enumerate(df.columns):
        print(f"{i}: {col}")

    print("\nPrimeras 5 filas:")
    print(df.head())