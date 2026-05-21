# Hiring Copilot Mini

A simple AI-executed candidate matching and recommendation web app.

The goal is **not just to score resumes**. The goal is to show how AI can execute a recruiting workflow and produce structured output that humans can validate, edit, and approve.

## What it does

The app supports this workflow:

```text
JD Intake
→ Role Requirement Understanding
→ Resume Evaluation
→ Recommendation Table
→ Strengths/Risks with Evidence
→ Recruiter Validation Questions
→ Client-Ready Candidate Summary
→ Human Validation
```

For each candidate, the app generates:

- Recommendation: `Ready to Submit`, `Validate First`, or `Do Not Submit`
- Overall score
- Brief reason
- Main risk
- Strengths with resume evidence
- Risks with resume evidence
- Recruiter validation questions
- Client-ready candidate summary
- Score breakdown by role criteria

## Tech stack

- Python
- Streamlit
- OpenAI Python SDK
- OpenAI-compatible LLM endpoint
- pypdf
- pandas

## Why this design

This prototype is intentionally lightweight because the assignment emphasizes product thinking, workflow understanding, fast prototyping, and human-in-the-loop recruiting operations.

The core product decision is to separate the workflow into two AI steps:

1. **Understand the JD first**
   - Extract must-have requirements
   - Extract nice-to-have requirements
   - Extract workflow/product/technical criteria
   - Create weighted evaluation criteria

2. **Evaluate each resume against the extracted role requirements**
   - Produce a recommendation
   - Give evidence-based strengths and risks
   - Ask validation questions instead of pretending AI is always certain
   - Prepare a client-ready summary for human review

This makes the system more explainable and easier for a recruiter to validate.

## Quick start

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/hiring-copilot-mini.git
cd hiring-copilot-mini
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Mac/Linux:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Optional: create local environment file

```bash
cp .env.example .env
```

Edit `.env`:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

You can also paste the API key directly into the app sidebar.

### 5. Run the app

```bash
streamlit run app.py
```

## Using other LLM providers

This app uses the OpenAI Python SDK with a configurable `base_url`, so it can work with many OpenAI-compatible providers.

Examples:

```env
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

For other providers, use their OpenAI-compatible endpoint and model name.

## How to publish on GitHub

1. Create a new GitHub repository.
2. Put these files in the repo.
3. Run:

```bash
git init
git add .
git commit -m "Initial Hiring Copilot Mini prototype"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/hiring-copilot-mini.git
git push -u origin main
```

## How to deploy

### Option A: Streamlit Community Cloud

1. Push the repo to GitHub.
2. Go to Streamlit Community Cloud.
3. Create a new app from the GitHub repo.
4. Set the main file path to:

```text
app.py
```

5. Add secrets if needed.

### Option B: Local demo

Run:

```bash
streamlit run app.py
```

## Suggested demo script

1. Upload the Applied AI Product Intern JD.
2. Upload several candidate resumes.
3. Click **Run Candidate Matching**.
4. Show the extracted role analysis.
5. Show the recommendation table.
6. Open one candidate detail panel.
7. Explain the human validation questions.
8. Edit the client-ready summary to show the human-in-the-loop step.

## Product tradeoffs

### What this prototype does well

- Simple and fast to build
- Easy to demo
- Customer can bring their own API key
- Produces structured recruiter-facing output
- Keeps humans in control
- Shows evidence instead of only a score

### What is intentionally not included

- Sourcing
- LinkedIn search
- Outreach automation
- ATS integration
- User authentication
- Database persistence
- Full audit log
- Multi-user approval workflow

## Future improvements

- Add database storage for JDs, candidates, and human edits
- Add recruiter approval status
- Add export to PDF or ATS format
- Add red-flag detection
- Add model comparison
- Add interview-kit generation
- Add candidate ranking explanations
- Add batch processing for larger resume sets
- Add role-specific scoring rubric editor
- Add structured feedback loop from recruiter decisions

## Responsible use

This tool should support recruiter judgment, not replace it. Human reviewers should validate all outputs before submission. Do not use protected-class information or irrelevant personal details in hiring decisions.
