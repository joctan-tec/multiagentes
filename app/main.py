from agents.graphs import construir_grafo_multiagente


def ejecutar_sistema(pregunta_usuario):
    grafo = construir_grafo_multiagente()
    estado_inicial = {"pregunta": pregunta_usuario}
    resultado = grafo.invoke(estado_inicial)

    print("\n✅ Respuesta final al usuario:")
    print(resultado["respuesta_final"])


if __name__ == "__main__":
    pregunta = "Cuantos dias de vacaciones le corresponden a un trabajador al adulto?"
    ejecutar_sistema(pregunta)
