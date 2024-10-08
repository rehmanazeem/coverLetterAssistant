import os
from openai import OpenAI

def createClient():
    client = OpenAI(
        base_url = 'http://localhost:11434/v1',
        api_key='ollama', # required, but unused
    )
    return client

def getFileContent(path : str, filename : str):
    with open(os.path.join(path,filename), 'r') as f:
        jobDescription = f.read()
    return jobDescription


BASE_DIR = './files'
jobDescriptionFilename = 'jobDescription.txt'
cvFilename = 'CV.txt'

jobDescription = getFileContent(BASE_DIR, jobDescriptionFilename)

summarizerPrompt = f"""
###
From the following job description :
{jobDescription}

Create and extract a summary that contain important details such as <Key responsibilities>, <Qualifications>, <Skills>, <Keywords>, <General Information>, <Job Title> and <Company Name>.
###

---
Arrange the summary in the following way :
1. Job Title: <Job Title>
2. Company Name: <Company Name>
3. General Information about the job: <General Information>
4. Key Responsibilities: <Key responsibilities>
5. Qualifications: <Qualifications>
6. Skills: <Skills>
7. Keywords: <Keywords>
---
"""

messages = [    
    {"role": "system", "content": summarizerPrompt},
    {"role": "user", "content": "Summarize the job description based on the system prompt."}
]

client = createClient()
response = client.chat.completions.create(
    model="llama3.2",
    temperature=0.7,
    messages=messages
    )

lineCount = 150
summarizedJobDescription = response.choices[0].message.content
# print("="*lineCount)
# print(summarizedJobDescription, sep="\n")
# print("="*lineCount)

cvContent = getFileContent(BASE_DIR, cvFilename)

# coverLetterWritingPrompt = f"""
# ###
# Based on the following job description summary:
# {summarizedJobDescription}

# And the following CV:
# {cvContent}

# Write a professional cover letter tailored to the job description. The cover letter should highlight relevant experiences, skills, and qualifications from the CV that match the job requirements. It should be structured as follows:

# 1. Introduction: Briefly introduce yourself and state the position you are applying for.
# 2. Body Paragraph 1: Discuss your relevant experience and how it aligns with the key responsibilities of the job.
# 3. Body Paragraph 2: Highlight your qualifications and skills that match the job requirements.
# 4. Body Paragraph 3: Mention any additional information or unique qualities that make you a strong candidate.
# 5. Conclusion: Express enthusiasm for the position and provide contact information for follow-up.
# ###

# ---
# Arrange the cover letter in the following way:
# 1. Introduction
# 2. Body Paragraph 1
# 3. Body Paragraph 2
# 4. Body Paragraph 3
# 5. Conclusion
# ---
# """

# messages = [    
#     {"role": "system", "content": coverLetterWritingPrompt},
#     {"role": "user", "content": "Write a cover letter based on the system prompt."}
# ]

# response = client.chat.completions.create(
#     model="llama3.2",
#     temperature=0.7,
#     messages=messages
# )

# coverLetter = response.choices[0].message.content
# print("="*lineCount)
# print(coverLetter, sep="\n")
# print("="*lineCount)


matchingSkillsPrompt = f"""
###
From the following job description summary:
{summarizedJobDescription}

And the following CV:
{cvContent}

Identify and list the matching skills, keywords, and relevant information between the job description and the CV. The list should be structured as follows:

1. Matching Skills: <List of matching skills>
2. Matching Keywords: <List of matching keywords>
3. Relevant Information: <List of relevant information>
###

Latly mention the job title and company name from the job description summary.
"""

messages = [    
    {"role": "system", "content": matchingSkillsPrompt},
    {"role": "user", "content": "Identify and list the matching skills, keywords, and relevant information based on the system prompt."}
]

response = client.chat.completions.create(
    model="llama3.2",
    temperature=0.7,
    messages=messages
)

matchedOutput = response.choices[0].message.content
print("="*lineCount)
print(matchedOutput, sep="\n")
print("="*lineCount)

coverLetterWritingPrompt = f"""
###
Based on the following matched output:
{matchedOutput}

Write a professional cover letter tailored to the job description. The cover letter should highlight relevant experiences, skills, and qualifications that match the job requirements. It should be structured as follows:

1. Introduction: Briefly introduce yourself and state the position you are applying for.
2. Body Paragraph 1: Discuss your relevant experience and how it aligns with the key responsibilities of the job. Here avoid repeating the information from the CV.
3. Body Paragraph 2: Highlight your qualifications and skills that match the job requirements primarily focusing on the matched skills and keywords.
4. Body Paragraph 3: Mention any additional information or unique qualities that make you a strong candidate, focusing on the relevant information.
5. Conclusion: Express enthusiasm for the position and provide contact information for follow-up.

Keep the cover letter concise and professional.
###

---
Arrange the cover letter in the following way:
1. Introduction
2. Body Paragraph 1
3. Body Paragraph 2
4. Body Paragraph 3
5. Conclusion
---
"""

messages = [    
    {"role": "system", "content": coverLetterWritingPrompt},
    {"role": "user", "content": "Write a cover letter based on the system prompt."}
]

response = client.chat.completions.create(
    model="llama3.2",
    temperature=0.7,
    messages=messages
)

coverLetter = response.choices[0].message.content
print("="*lineCount)
print(coverLetter, sep="\n")
print("="*lineCount)

