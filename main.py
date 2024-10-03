import os
from openai import OpenAI

def createClient():
    client = OpenAI(
        base_url = 'http://localhost:11434/v1',
        api_key='ollama', # required, but unused
    )
    return client

with open('./files/jobDescription.txt', 'r') as f:
    jobDescription = f.read()

summarizer_prompt = f"""
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
    {"role": "system", "content": summarizer_prompt},
    {"role": "user", "content": "Summarize the job description based on the system prompt."}
]

client = createClient()
response = client.chat.completions.create(
    model="llama3.2",
    temperature=0.7,
    messages=messages
    )

lineCount = 150
wrapped_output = response.choices[0].message.content
print("="*lineCount)
print(wrapped_output, sep="\n")
print("="*lineCount)