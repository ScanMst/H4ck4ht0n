import pandas as pd
from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

docs = list(db.tableau_recommendations.find({}, {"_id": 0}))

if not docs:
    print("No hay datos en tableau_recommendations")
    exit()

df = pd.DataFrame(docs)

output = "data/tableau_recommendations.csv"

df.to_csv(
    output,
    index=False,
    encoding="utf-8-sig"
)

print(f"Archivo generado: {output}")
print(f"Registros exportados: {len(df)}")
print("\nColumnas:")
print(list(df.columns))