# LangGraph Research Assistant

A 4-agent research assistant built with LangGraph as a prototype for exploring graph-based multi-agent orchestration. Built alongside a parallel [CrewAI implementation](https://github.com/radfordalex/crewai-research-assistant) to compare role-based vs graph-based orchestration patterns.

Things are getting meta, folks — we're using agentic frameworks to research the newest developments in agentic AI.

## Architecture

Four agents wired as nodes in a sequential state graph:

```
[Research Planner] → [Web Researcher] → [Quality Checker] → [Report Writer] → END
```

**Research Planner** — Decomposes a query into 3-5 focused sub-questions with rationale and suggested search terms. Pure reasoning, no tools.

**Web Researcher** — Searches the web for each sub-question using Tavily, organizes findings with source URLs, key facts, and confidence levels.

**Quality Checker** — Reviews all findings for accuracy. Rates sources 1-5, flags unsupported claims, identifies contradictions, and notes research gaps.

**Report Writer** — Synthesizes validated findings into a structured Markdown report with inline citations, a limitations section, and a full source list. Saves to `output/report.md`.

## How It Works

Every agent is the same LLM (GPT-4o-mini) receiving different instructions. The "multi-agent" behavior comes from the orchestration — each node gets a different system prompt (role, goal, task) and reads from / writes to a shared `ResearchState` that flows through the graph.

```python
# state.py — the shared clipboard
class ResearchState(TypedDict):
    query: str
    sub_questions: Optional[str]
    research_findings: Optional[str]
    quality_assessment: Optional[str]
    final_report: Optional[str]
```

```python
# graph.py — the wiring
workflow.set_entry_point("planner")
workflow.add_edge("planner", "researcher")
workflow.add_edge("researcher", "quality_checker")
workflow.add_edge("quality_checker", "report_writer")
workflow.add_edge("report_writer", END)
```

## Setup

### Prerequisites
- Python 3.10+
- OpenAI API key
- Tavily API key (free tier: 1,000 searches/month at https://tavily.com)

### Installation

```bash
git clone https://github.com/radfordalex/langgraph-research-assistant.git
cd langgraph-research-assistant
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate

pip install langgraph langchain-openai langchain-tavily langchain-community python-dotenv
```

### Configuration

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your-openai-key
TAVILY_API_KEY=your-tavily-key
```

## Usage

```bash
python main.py
```

To change the research query, edit the `query` string in `main.py`:

```python
inputs = {
    "query": "Your research question here",
}
```

Report saves to `output/report.md`.

## File Structure

```
langgraph-research-assistant/
├── state.py    # ResearchState TypedDict — shared state between nodes
├── tools.py    # Tavily search tool setup
├── agents.py   # 4 node functions (planner, researcher, quality_checker, report_writer)
├── graph.py    # StateGraph wiring: nodes + edges
├── main.py     # Entry point
└── .env        # API keys (not committed)
```

## Comparison with CrewAI Version

This prototype was built alongside a [CrewAI implementation](https://github.com/radfordalex/crewai-research-assistant) of the same 4-agent pipeline. Key differences:

| | LangGraph | CrewAI |
|---|---|---|
| **Orchestration** | Graph-based — you define nodes and edges explicitly | Role-based — you define agents with roles/goals/backstories |
| **Config** | Pure Python, no YAML | YAML configs for agents and tasks |
| **Control** | Full control over flow, supports conditional edges and loops | Framework manages flow, sequential or hierarchical |
| **Setup** | `pip install` + write Python | CLI scaffolding with `crewai create crew` |
| **Best for** | Production systems needing complex routing | Rapid prototyping and learning agent concepts |

Both produce comparable research reports from the same query. The difference is in how you think about the problem: CrewAI thinks in roles, LangGraph thinks in graphs.

## Evolution

This prototype led to an upgraded production version: [agentic-ai-weekly](https://github.com/radfordalex/agentic-ai-weekly), which adds semantic chunking, multi-pass search, and a quality retry loop.

## Tech Stack

- **Orchestration**: LangGraph
- **LLM**: GPT-4o-mini
- **Search**: Tavily Search API
