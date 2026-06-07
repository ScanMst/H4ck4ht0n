from config import MONGO_URI, DB_NAME, OPENROUTER_API_KEY

print("Mongo:", MONGO_URI is not None)
print("DB:", DB_NAME)
print("OpenRouter:", OPENROUTER_API_KEY is not None)

if OPENROUTER_API_KEY:
    print("OpenRouter inicio:", OPENROUTER_API_KEY[:10])