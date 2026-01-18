from typing import TypedDict, Optional, List
from langgraph.graph import StateGraph, END, START
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
from .prompts import system_prompt
import os
from .retrieval_es import Retrieval

load_dotenv()

# State defining
class AgentState(TypedDict):
    question: str
    documents: List[str]
    answer: Optional[str]

# Agent
class MedAgent:
    def __init__(self, cfg, retriever):
        self.model_name = cfg.generator.model
        self.retriever = retriever
        self.system_prompt = system_prompt

        self._init_model()
        self._build_graph()

    def _init_model(self):
        self.model = ChatGoogleGenerativeAI(
            model=self.model_name,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
        )

    def _build_graph(self):
        graph = StateGraph(AgentState)

        graph.add_node("retrieval", self.retrieval_node)
        graph.add_node("generation", self.generation_node)

        graph.add_edge(START, "retrieval")
        graph.add_edge("retrieval", "generation")
        graph.add_edge("generation", END)

        self.med_graph = graph.compile()

    # ---------------- NODES ----------------
    def retrieval_node(self, state: AgentState):
        docs = self.retriever.querying(state["question"])
        docs = [i["record"] for i in docs]
        return {"documents": docs}

    def generation_node(self, state: AgentState):
        context = "\n\n".join(state["documents"])

        messages = [
            SystemMessage(content=self.system_prompt.format(context=context)),
            HumanMessage(content=state["question"]),
        ]

        response = self.model.invoke(messages)
        return {"answer": response.content}



# sanity checking
if __name__ == "__main__":
    import yaml
    from munch import Munch
    with open('config/main.yaml', 'r') as f:
        config = yaml.safe_load(f)
        config = Munch.fromDict(config)
    retrieval = Retrieval(config)
    # creating indexing
    # retrieval.indexing()
    agent = MedAgent(config, retrieval)
    result = agent.med_graph.invoke({
        "question": "Did Mohs micrographic surgery fixed-tissue technique for melanoma of the nose?"
    })
    print(result["answer"])
    print("\n\n------------------------------")
    print(result["documents"])