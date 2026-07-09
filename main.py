"""
Entry point for the cover letter generation pipeline.

Steps:
  1. Load job description and CV from files/.
  2. Summarise the job description.
  3. Draft a cover letter from the JD summary and CV.
  4. Refine the draft for a better skills match.

Usage:
    python main.py
"""

from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate

from assistant import CoverLetterAssistant
from prompts import SYSTEM_PROMPT, SUMMARY_HUMAN_MESSAGE, WRITER_HUMAN_MESSAGE, REFINEMENT_HUMAN_MESSAGE

BASE_DIR = Path('./files')
SEP = "=" * 100


def main():
    job_description = (BASE_DIR / 'jobDescription.txt').read_text()
    cv = (BASE_DIR / 'CV.txt').read_text()

    assistant = CoverLetterAssistant(model_name='llama3.2')

    prompt = ChatPromptTemplate([
        ('system', SYSTEM_PROMPT),
        ('human', SUMMARY_HUMAN_MESSAGE),
    ])

    # Step 1: summarise the job description
    jd_summary = assistant.get_response(prompt.invoke({'job_description': job_description}))
    prompt.append(('ai', jd_summary))
    prompt.append(('human', WRITER_HUMAN_MESSAGE))

    # Step 2: draft the cover letter
    cover_letter = assistant.get_response(prompt.invoke({
        'job_description': job_description,
        'job_description_summary': jd_summary,
        'cv': cv,
    }))
    print(cover_letter)
    print(SEP)

    # Step 3: refine the draft
    prompt.append(('human', REFINEMENT_HUMAN_MESSAGE))
    cover_letter = assistant.get_response(prompt.invoke({
        'job_description': job_description,
        'job_description_summary': jd_summary,
        'cv': cv,
        'cover_letter': cover_letter,
    }))
    print(cover_letter)


if __name__ == "__main__":
    main()
