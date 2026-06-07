from score_adjuster import ajustar_score_por_aprendizaje

score, motivo = ajustar_score_por_aprendizaje(
    producto="Powerade Moras",
    tipo_recomendacion="oportunidad_cedis",
    score_original=88
)

print("Score ajustado:", score)
print("Motivo:", motivo)