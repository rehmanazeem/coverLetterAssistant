"""Prompt strings for the cover letter generation pipeline."""

SYSTEM_PROMPT = (
    "You are an AI assistant who drafts cover letters based on words, skills, "
    "and keywords matched from the job description and the candidate's CV."
)

SUMMARY_HUMAN_MESSAGE = """Here is the job description that I would like you to summarize:
{job_description}

Summarize the job description and extract the following information:
    - Job Title
    - Company Name
    - Key responsibilities
    - Required Qualifications
    - Skills
    - Important Keywords
    - General summary
"""

WRITER_HUMAN_MESSAGE = """Here is the CV and the job description summary to write a cover letter from:

---
CV: {cv}
Job description summary: {job_description_summary}
---

Write a cover letter based on the information in both documents. Include only the most relevant factual information.
Avoid paraphrasing sentences from the CV — be creative in how you present the information.
Output the body of the cover letter only.
"""

REFINEMENT_HUMAN_MESSAGE = (
    "Take this cover letter: {cover_letter} "
    "Further optimise it to better match the experience, skills, and information in the previously mentioned CV."
)
