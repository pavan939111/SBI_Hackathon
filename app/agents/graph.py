"""
LangGraph construction mapping Samjho, Khojo, Chalao, Queue Hatao, and Suraksha nodes.
"""
from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.samjho.agent import samjho_node
from app.agents.khojo.agent import khojo_node
from app.agents.chalao.agent import chalao_node
from app.agents.queue_hatao.agent import queue_hatao_node
from app.agents.suraksha.agent import suraksha_node

def build_graph() -> StateGraph:
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("samjho", samjho_node)
    workflow.add_node("khojo", khojo_node)
    workflow.add_node("chalao", chalao_node)
    workflow.add_node("queue_hatao", queue_hatao_node)
    workflow.add_node("suraksha", suraksha_node)
    
    # Set entry point
    workflow.set_entry_point("samjho")
    
    # Define route steps
    workflow.add_conditional_edges(
        "samjho",
        lambda state: state.get("intent", "general_query"),
        {
            "loan_inquiry": "khojo",
            "general_query": "chalao",
            "fraud_alert": "suraksha",
            "appointment": "queue_hatao"
        }
    )
    
    workflow.add_edge("khojo", "chalao")
    workflow.add_edge("chalao", "queue_hatao")
    workflow.add_edge("queue_hatao", "suraksha")
    workflow.add_edge("suraksha", END)
    
    return workflow.compile()
