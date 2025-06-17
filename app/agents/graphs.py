from langgraph.graph import StateGraph, END
from open_ai_conf import Config
from agents.agents import AgenteBuscador, AgenteAnalista, AgenteRedactor


def construir_grafo_multiagente():
    # retriever = Config().crear_retriever()
    buscador = AgenteBuscador()
    analista = AgenteAnalista()
    redactor = AgenteRedactor()

    def nodo_buscador(state):
        return buscador.ejecutar(state["pregunta"])

    def nodo_analista(state):
        return analista.ejecutar(state["documentos"], state["pregunta"])

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