from agents.graphs import construir_grafo_multiagente
from text_processor.load_pdf import main as cargar_pdf

def ejecutar_sistema(pregunta_usuario):
    grafo = construir_grafo_multiagente()
    estado_inicial = {"pregunta": pregunta_usuario}
    resultado = grafo.invoke(estado_inicial)

    print("\nRespuesta final al usuario:")
    print(resultado["respuesta_final"])


if __name__ == "__main__":
    cargar_pdf()  # Cargar PDFs antes de ejecutar el sistema
    
    
