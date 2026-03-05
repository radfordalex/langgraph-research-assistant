from typing import TypedDict, Optional

class ResearchState(TypedDict):
    query: str
    sub_questions: Optional[str]
    research_findings: Optional[str]
    quality_assessment: Optional[str]
    final_report: Optional[str]
