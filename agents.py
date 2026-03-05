from langchain_openai import ChatOpenAI
from tools import search_tool
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def research_planner(state):
    query = state["query"]
    response = llm.invoke(
        f"""You are a Research Strategist. Your goal is to decompose research queries 
        into focused, searchable sub-questions.

        Analyze this research query and decompose it into 3-5 focused sub-questions 
        that together would provide a comprehensive answer:

        QUERY: {query}

        For each sub-question provide:
        1. The sub-question itself
        2. Why this aspect matters
        3. Suggested search terms

        Format as a numbered list."""
    )
    return {"sub_questions": response.content}


def web_researcher(state):
    sub_questions = state["sub_questions"]
    all_findings = []

    for line in sub_questions.split("\n"):
        if line.strip() and line.strip()[0].isdigit():
            results = search_tool.invoke(line.strip()[:200])
            all_findings.append(f"Sub-question: {line.strip()}\nFindings: {results}\n")

    findings_text = "\n---\n".join(all_findings)

    response = llm.invoke(
        f"""You are an Information Retrieval Specialist. Your goal is to find 
        authoritative, recent sources.

        Organize these raw search results into structured findings. For each 
        sub-question, provide:
        - Source name and URL
        - Key findings (specific facts, not vague summaries)
        - Publication date if available
        - Any gaps where information was not found

        NEVER fabricate URLs. Only report URLs that appear in the search results.

        RAW RESULTS:
        {findings_text}"""
    )
    return {"research_findings": response.content}


def quality_checker(state):
    findings = state["research_findings"]
    response = llm.invoke(
        f"""You are a Fact-Checker and Source Evaluator. You are skeptical by nature.

        Review these research findings and assess:
        1. Is each claim clearly supported by the cited source?
        2. Source quality rating (1-5): Is it authoritative? Current? Primary source?
        3. Are there contradictions between sources?
        4. Are there claims that appear unsupported or potentially hallucinated?

        Format your response with these sections:
        CONFIRMED: [findings that are well-supported]
        FLAGGED: [claims that need verification]
        CONTRADICTIONS: [conflicting information between sources]
        SOURCE RATINGS: [1-5 rating for each source with justification]
        GAPS: [important aspects not covered]

        FINDINGS TO REVIEW:
        {findings}"""
    )
    return {"quality_assessment": response.content}


def report_writer(state):
    findings = state["research_findings"]
    quality = state["quality_assessment"]
    query = state["query"]
    response = llm.invoke(
        f"""You are a Research Report Writer. Create a polished Markdown report.

        Requirements:
        - Clear title and executive summary (2-3 sentences)
        - Organized sections addressing each major aspect of the query
        - Inline citations linking to source URLs
        - A Limitations and Uncertainties section using the quality assessment
        - A Sources section at the end with all referenced URLs
        - Write for a technical audience but keep it accessible

        ORIGINAL QUERY: {query}
        RESEARCH FINDINGS: {findings}
        QUALITY ASSESSMENT: {quality}"""
    )
    return {"final_report": response.content}