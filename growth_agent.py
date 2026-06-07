from openai import OpenAI
from config import OPENROUTER_API_KEY

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)


def generar_recomendacion(contexto_cliente: dict) -> str:
    protopersona = contexto_cliente.get("protopersona", "madre_emprendedora")

    perfiles = {
        "madre_emprendedora": {
            "nombre_demo": "Fernanda",
            "tono": "directo, práctico y enfocado en ahorrar tiempo",
            "necesidad": "quiere que la tienda funcione sin estar encima todo el día",
            "intro": "Encontramos oportunidades rápidas para ayudarte a vender más esta semana."
        },
        "dueno_apoyado": {
            "nombre_demo": "Raúl",
            "tono": "muy simple, paciente y sin tecnicismos",
            "necesidad": "prefiere pedidos fáciles y apoyo claro porque no le gusta complicarse con tecnología",
            "intro": "Te dejamos recomendaciones simples para que puedas pedir sin complicarte."
        },
        "familiar_comprometida": {
            "nombre_demo": "Fernanda",
            "tono": "claro, cuidadoso y orientado a estabilidad familiar",
            "necesidad": "necesita mantener la tienda funcionando con instrucciones simples y seguimiento claro",
            "intro": "Encontramos opciones claras para mantener la tienda surtida y estable."
        }
    }

    perfil = perfiles.get(protopersona, perfiles["madre_emprendedora"])

    cliente_nombre = contexto_cliente.get("cliente_alias")
    if not cliente_nombre:
        cliente_nombre = perfil["nombre_demo"]

    recomendaciones = contexto_cliente.get("recomendaciones", [])
    loyalty = contexto_cliente.get("loyalty", {})

    productos_recomendados = [
        r.get("producto") for r in recomendaciones if r.get("producto")
    ]

    prompt = f"""
Eres el Growth Agent de Tuali.

Estás hablando directamente con la persona usuaria dentro de la app Tuali.

Nombre a mostrar:
{cliente_nombre}

Protopersona:
{protopersona}

Tono recomendado:
{perfil["tono"]}

Necesidad principal:
{perfil["necesidad"]}

Contexto calculado por el motor de recomendaciones:
{contexto_cliente}

REGLAS OBLIGATORIAS:
- Habla en segunda persona: "tú", "tu tienda", "tu pedido", "te recomendamos".
- No hables como directivo.
- No uses tecnicismos.
- No inventes productos.
- No inventes descuentos.
- No inventes fechas.
- No inventes porcentajes.
- No inventes impactos.
- Usa únicamente la evidencia, motivo, predicción, impacto y acción que vienen en recomendaciones.
- En "Productos recomendados para ti" lista únicamente estos productos:
{productos_recomendados}
- No uses productos de pedido_sugerido si no aparecen en recomendaciones.
- No agregues productos extra.
- Si falta alguna recomendación, no inventes otra.
- Mantén el texto breve, claro y accionable.
- La respuesta debe parecer una pantalla dentro de una app móvil.

DATOS PRINCIPALES:

Recomendaciones:
{recomendaciones}

Loyalty:
{loyalty}

FORMATO OBLIGATORIO:

Hola, {cliente_nombre} 👋

{perfil["intro"]}

🔍 Buscar productos

══════════════════════════════

✨ Oportunidades para crecer

🔁 Reabastecer [producto del tipo reabastecimiento]
Evidencia: [evidencia exacta]
Motivo: [motivo exacto]
Predicción: [predicción exacta] probabilidad de que te convenga.
Impacto esperado: [impacto exacto]
Acción sugerida: [acción exacta]
[Agregar] [No me interesa]

⭐ Nuevo para tu tienda
Evidencia: [evidencia exacta del tipo oportunidad_cedis]
Motivo: [motivo exacto]
Predicción: [predicción exacta] probabilidad de que te convenga.
Impacto esperado: [impacto exacto]
Acción sugerida: [acción exacta]
[Agregar] [No me interesa]

🔥 Promoción disponible
Evidencia: [evidencia exacta del tipo promocion]
Motivo: [motivo exacto]
Predicción: [predicción exacta] probabilidad de que te convenga.
Impacto esperado: [impacto exacto]
Acción sugerida: [acción exacta]
[Agregar] [No me interesa]

🏆 Tus puntos
Puntos actuales: {loyalty.get("puntos_actuales", 0)}
Oportunidad: {loyalty.get("beneficio", loyalty.get("regla", "Puedes sumar puntos con tus compras en Tuali."))}
[Ver recompensas]

══════════════════════════════

Productos recomendados para ti

- [producto del tipo reabastecimiento]
Razón: [usa solo el motivo de esa recomendación]

- [producto del tipo oportunidad_cedis]
Razón: [usa solo el motivo de esa recomendación]

- [producto del tipo promocion]
Razón: [usa solo el motivo de esa recomendación]

Pregunta de aprendizaje:
¿Te sirvieron estas recomendaciones?
[Sí] [No] [Más tarde]
"""

    response = client.chat.completions.create(
        model="meta-llama/llama-3.1-8b-instruct",
        messages=[
            {
                "role": "system",
                "content": (
                    "Eres un agente de crecimiento dentro de la app Tuali. "
                    "Solo explicas recomendaciones ya calculadas por un motor de datos. "
                    "No inventes productos, descuentos, fechas, porcentajes ni impactos. "
                    "Adapta el tono según la protopersona."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content