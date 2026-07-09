# cover-letter-assistant

A local-LLM tool that generates tailored cover letters from a job description and CV using a locally-hosted Ollama model.

## Project structure

```
coverLetterAssistant/
├── files/          # Your CV and job description (gitignored)
│   ├── CV.txt
│   └── jobDescription.txt
├── assistant.py    # CoverLetterAssistant class (LLM wrapper)
├── prompts.py      # Prompt strings for each pipeline step
├── main.py         # Entry point
└── requirements.txt
```

## Pipeline

1. **Summarise** — extracts job title, responsibilities, skills, and keywords from the JD
2. **Draft** — writes a cover letter matched to the JD summary and CV
3. **Refine** — optimises the draft for a closer skills and experience match

## Setup

**1. Install and start Ollama, then pull the model**
```bash
ollama pull llama3.2
```

**2. Install Python dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your files**

Place your CV and job description as plain text in the `files/` directory:
```
files/CV.txt
files/jobDescription.txt
```

## Usage

```bash
python main.py
```

Prints the initial draft, a separator, then the refined cover letter.

## Data

`files/` is gitignored — your CV and job description are never committed.
