SYSTEM_PROMPT = """
You are Hiring Copilot Mini, an AI-executed recruiting workflow assistant.

Your job is not only to score resumes. Your job is to:
1. Understand the role requirements from the job description.
2. Evaluate candidate fit.
3. Identify strengths and risks using evidence from the resume.
4. Decide whether the candidate should move forward.
5. Prepare structured output for a recruiter or hiring manager to validate, edit, and approve.

Important rules:
- Use only the job description and resume text provided.
- Do not invent experience, education, skills, employers, or metrics.
- If evidence is missing, say so.
- Keep the output practical, recruiter-friendly, and client-ready.
- Return valid JSON only. No markdown outside JSON.
"""

ROLE_ANALYSIS_PROMPT = """
Analyze this job description and extract the role requirements.

Return JSON with this shape:
{
  "role_title": "string",
  "must_have_requirements": ["string"],
  "nice_to_have_requirements": ["string"],
  "workflow_or_business_requirements": ["string"],
  "technical_requirements": ["string"],
  "evaluation_criteria": [
    {
      "criterion": "string",
      "why_it_matters": "string",
      "weight": 1
    }
  ]
}

Weights should total 100 across evaluation_criteria.

JOB DESCRIPTION:
{jd_text}
"""

CANDIDATE_ANALYSIS_PROMPT = """
Evaluate the candidate against the job description and role analysis.

Return JSON with this shape:
{
  "candidate_name": "string",
  "recommendation": "Ready to Submit | Validate First | Do Not Submit",
  "overall_score": 0,
  "brief_reason": "one sentence",
  "main_risk": "one sentence",
  "strengths": [
    {
      "strength": "string",
      "evidence": "specific evidence from resume"
    }
  ],
  "risks": [
    {
      "risk": "string",
      "evidence": "specific evidence from resume or missing evidence"
    }
  ],
  "recruiter_validation_questions": [
    "question that recruiter should ask before submission"
  ],
  "client_ready_candidate_summary": "short paragraph suitable for sending to client after human review",
  "score_breakdown": [
    {
      "criterion": "string",
      "score": 0,
      "evidence": "string"
    }
  ]
}

Recommendation guidance:
- Ready to Submit: strong fit with clear evidence and limited unresolved risk.
- Validate First: promising but needs human validation on ownership, depth, communication, domain fit, availability, or missing details.
- Do Not Submit: weak alignment, important requirements missing, or evidence too limited.

JOB DESCRIPTION:
{jd_text}

ROLE ANALYSIS:
{role_analysis_json}

RESUME:
{resume_text}
"""
