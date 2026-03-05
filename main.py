from graph import app
from dotenv import load_dotenv
import os

load_dotenv()

def run():
    inputs = {
        "query": "What are the leading multi-agent AI frameworks and how do they compare for building production agentic systems?",
        "sub_questions": None,
        "research_findings": None,
        "quality_assessment": None,
        "final_report": None,
    }

    print("Starting LangGraph Research Assistant...\n")

    for step in app.stream(inputs):
        node_name = list(step.keys())[0]
        print(f"\n{'='*60}")
        print(f"Completed: {node_name}")
        print(f"{'='*60}")

        node_output = step[node_name]
        for key, value in node_output.items():
            if value:
                print(f"\n{key}:\n{value[:500]}...")

    # Save final report
    final_state = list(step.values())[0]
    if "final_report" in final_state and final_state["final_report"]:
        os.makedirs("output", exist_ok=True)
        with open("output/report.md", "w") as f:
            f.write(final_state["final_report"])
        print(f"\n\nReport saved to output/report.md")

if __name__ == "__main__":
    run()