from __future__ import annotations

import json
import os
from typing import Any

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from core.llm_client import call_llm_json
from core.pdf_utils import extract_pdf_text, truncate_text
from core.prompts import SYSTEM_PROMPT, ROLE_ANALYSIS_PROMPT, CANDIDATE_ANALYSIS_PROMPT

load_dotenv()

st.set_page_config(page_title="Hiring Copilot Mini", page_icon="🤝", layout="wide")

st.title("🤝 Hiring Copilot Mini")
st.caption(
    "AI-executed candidate matching workflow: JD intake → fit analysis → recommendation → human validation."
)

with st.sidebar:
    st.header("LLM Settings")
    api_key = st.text_input(
        "API Key",
        type="password",
        value=os.getenv("OPENAI_API_KEY", ""),
        help="Paste your own API key. It is only used for this session.",
    )
    base_url = st.text_input(
        "Base URL",
        value=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        help="Use OpenAI or any OpenAI-compatible endpoint.",
    )
    model = st.text_input(
        "Model",
        value=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        help="Example: gpt-4o-mini, gpt-4.1-mini, claude/openai-compatible gateway model, etc.",
    )
    temperature = st.slider("Temperature", 0.0, 1.0, 0.1, 0.1)

st.subheader("1. Upload job description and resumes")

left, right = st.columns(2)
with left:
    jd_file = st.file_uploader("Job Description PDF", type=["pdf"], accept_multiple_files=False)
with right:
    resume_files = st.file_uploader("Candidate Resume PDFs", type=["pdf"], accept_multiple_files=True)

run_btn = st.button("Run Candidate Matching", type="primary", disabled=not jd_file or not resume_files)

def safe_get(d: dict[str, Any], key: str, default: Any = "") -> Any:
    value = d.get(key, default)
    return default if value is None else value

if run_btn:
    if not api_key:
        st.error("Please enter an API key in the sidebar.")
        st.stop()

    with st.spinner("Reading PDFs..."):
        jd_text = truncate_text(extract_pdf_text(jd_file), 22000)
        resumes = []
        for file in resume_files:
            resumes.append(
                {
                    "filename": file.name,
                    "text": truncate_text(extract_pdf_text(file), 18000),
                }
            )

    with st.spinner("Understanding role requirements from the JD..."):
        role_analysis = call_llm_json(
            api_key=api_key,
            base_url=base_url,
            model=model,
            temperature=temperature,
            system_prompt=SYSTEM_PROMPT,
            # Use replace instead of format to avoid KeyError from JSON braces
            user_prompt=ROLE_ANALYSIS_PROMPT.replace("{jd_text}", jd_text),
        )

    st.subheader("2. Role Requirement Understanding")
    with st.expander("View extracted role analysis", expanded=True):
        st.json(role_analysis)

    results = []
    progress = st.progress(0)
    for i, resume in enumerate(resumes, start=1):
        with st.spinner(f"Evaluating {resume['filename']}..."):
            result = call_llm_json(
                api_key=api_key,
                base_url=base_url,
                model=model,
                temperature=temperature,
                system_prompt=SYSTEM_PROMPT,
                # Build the user prompt by replacing placeholders to avoid
                # interpreting JSON braces as format fields.
                user_prompt=(
                    CANDIDATE_ANALYSIS_PROMPT
                    .replace("{jd_text}", jd_text)
                    .replace(
                        "{role_analysis_json}",
                        json.dumps(role_analysis, ensure_ascii=False, indent=2),
                    )
                    .replace("{resume_text}", resume["text"])
                ),
            )
            result["source_file"] = resume["filename"]
            results.append(result)
        progress.progress(i / len(resumes))

    st.subheader("3. Recommendation Table")

    table_rows = []
    for r in results:
        table_rows.append(
            {
                "Candidate": safe_get(r, "candidate_name", r.get("source_file", "Unknown")),
                "Recommendation": safe_get(r, "recommendation"),
                "Score": safe_get(r, "overall_score"),
                "Brief Reason": safe_get(r, "brief_reason"),
                "Main Risk": safe_get(r, "main_risk"),
                "Source File": safe_get(r, "source_file"),
            }
        )

    df = pd.DataFrame(table_rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download recommendation table as CSV",
        data=csv,
        file_name="candidate_recommendations.csv",
        mime="text/csv",
    )

    st.subheader("4. Human Validation Workspace")
    for r in results:
        name = safe_get(r, "candidate_name", r.get("source_file", "Unknown"))
        rec = safe_get(r, "recommendation")
        score = safe_get(r, "overall_score")
        with st.expander(f"{name} — {rec} — Score: {score}", expanded=False):
            c1, c2 = st.columns(2)

            with c1:
                st.markdown("#### Strengths with Evidence")
                for item in safe_get(r, "strengths", []):
                    st.markdown(f"**{item.get('strength', '')}**")
                    st.write(item.get("evidence", ""))

                st.markdown("#### Risks with Evidence")
                for item in safe_get(r, "risks", []):
                    st.markdown(f"**{item.get('risk', '')}**")
                    st.write(item.get("evidence", ""))

            with c2:
                st.markdown("#### Recruiter Validation Questions")
                for q in safe_get(r, "recruiter_validation_questions", []):
                    st.checkbox(q, key=f"{name}-{q}")

                st.markdown("#### Client-Ready Candidate Summary")
                summary = st.text_area(
                    "Editable summary",
                    value=safe_get(r, "client_ready_candidate_summary"),
                    height=180,
                    key=f"summary-{name}",
                )

            st.markdown("#### Score Breakdown")
            breakdown = safe_get(r, "score_breakdown", [])
            if breakdown:
                st.dataframe(pd.DataFrame(breakdown), use_container_width=True, hide_index=True)

            st.markdown("#### Raw JSON")
            st.json(r)

    st.success("Workflow complete. Recruiter can now validate, edit, and approve outputs.")
else:
    st.info("Upload one JD PDF and one or more resume PDFs, then run candidate matching.")

st.markdown("---")
st.caption(
    "Prototype note: This demo uses customer-provided API credentials and an OpenAI-compatible endpoint. "
    "Do not upload confidential resumes unless your deployment, model provider, and data policy allow it."
)
