from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

print("=" * 60)
print("VALIDACION MONGODB")
print("=" * 60)

print("\nBase de datos:")
print(DB_NAME)

print("\nColecciones:")
for col in db.list_collection_names():
    print("-", col)

print("\n" + "=" * 60)

# tableau_recommendations
if "tableau_recommendations" in db.list_collection_names():

    total = db.tableau_recommendations.count_documents({})

    print("\nTABLEAU_RECOMMENDATIONS")
    print("Total registros:", total)

    ultimo = db.tableau_recommendations.find_one(
        sort=[("_id", -1)]
    )

    if ultimo:
        print("\nÚltima recomendación:")
        print("Cliente:", ultimo.get("cliente_alias"))
        print("CEDIS:", ultimo.get("cedis"))
        print("Producto:", ultimo.get("producto"))
        print("Tipo:", ultimo.get("tipo"))
        print("Score:", ultimo.get("score"))

print("\n" + "=" * 60)

# feedback
if "feedback" in db.list_collection_names():

    total = db.feedback.count_documents({})

    print("\nFEEDBACK")
    print("Total registros:", total)

    ultimo = db.feedback.find_one(
        sort=[("_id", -1)]
    )

    if ultimo:
        print("\nÚltimo feedback:")
        print("Producto:", ultimo.get("producto"))
        print("Respuesta:", ultimo.get("respuesta"))
print("\n" + "=" * 60)

# learning_summary
if "learning_summary" in db.list_collection_names():

    total = db.learning_summary.count_documents({})

    print("\nLEARNING SUMMARY")
    print("Total registros:", total)

    ultimo = db.learning_summary.find_one(
        sort=[("_id", -1)]
    )

    if ultimo:
        print("\nÚltimo aprendizaje:")
        print("Producto:", ultimo.get("producto"))
        print("Aceptación:", ultimo.get("tasa_aceptacion"))
        print("Aprendizaje:", ultimo.get("aprendizaje"))

print("\n" + "=" * 60)

print("\nValidación final completada.")