from langgraph.graph import StateGraph, END
from app.agents import AgenteBuscador, AgenteAnalista, AgenteRedactor

class GrafoMultiagente:
    """
    Clase que representa un grafo de estados para el flujo multiagente.
    Este grafo coordina las acciones de los agentes Buscador, Analista y Redactor.
    """

    def construir_grafo_multiagente(self, respuesta_anterior=None):
        """
        Construye un grafo de estados para el flujo multiagente.
        Este grafo coordina las acciones de los agentes Buscador, Analista y Redactor.
        Args:
            respuesta_anterior (str, optional): Respuesta previa del analista para continuar el flujo.
        Returns:
            StateGraph: Un grafo de estados que representa el flujo multiagente.
        """
        buscador = AgenteBuscador()
        analista = AgenteAnalista()
        redactor = AgenteRedactor()

        def nodo_buscador(state):
            return buscador.ejecutar(state["pregunta"])

        def nodo_analista(state):
            return analista.ejecutar(state["documentos"], state["pregunta"], respuesta_anterior)

        def nodo_redactor(state):
            return redactor.ejecutar(state["respuesta_analista"])

        builder = StateGraph(dict)
        builder.add_node("buscador", nodo_buscador)
        builder.add_node("analista", nodo_analista)
        builder.add_node("redactor", nodo_redactor)

        builder.set_entry_point("buscador")
        builder.add_edge("buscador", "analista")
        builder.add_edge("analista", "redactor")
        builder.add_edge("redactor", END)

        return builder.compile()