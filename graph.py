from langgraph.graph import StateGraph, END
from state import ResearchState
from agents import research_planner, web_researcher, quality_checker, report_writer

# Create the graph
workflow = StateGraph(ResearchState)

# Add nodes (each agent is a node)
workflow.add_node("planner", research_planner)
workflow.add_node("researcher", web_researcher)
workflow.add_node("quality_checker", quality_checker)
workflow.add_node("report_writer", report_writer)

# Add edges (the flow between agents)
workflow.set_entry_point("planner")
workflow.add_edge("planner", "researcher")
workflow.add_edge("researcher", "quality_checker")
workflow.add_edge("quality_checker", "report_writer")
workflow.add_edge("report_writer", END)

# Compile the graph
app = workflow.compile()