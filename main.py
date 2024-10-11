
### ==================================================================================================
### Code Overview:
### ==================================================================================================
### Section 1 : Importing required libraries
### Section 2 : Helper functions
### Section 3 : Paths and filenames
### Section 4 : Prompts for the AI model
### Section 5 : Messages for the AI model
### Section 6 : Main function
### ==================================================================================================

# **************************************** BEGINNINNG OF CODE ****************************************

### ==================================================================================================
### Section 1 : Importing required libraries
### ==================================================================================================
import os
from openai import OpenAI


### ==================================================================================================
### Section 2 : Helper functions
### ==================================================================================================
# Helper function to read the content of a file
def getFileContent(path : str, filename : str):
    with open(os.path.join(path,filename), 'r') as f:
        fileConent = f.read()
    return fileConent

# Helper function to create the OpenAI client
def createClient():
    client = OpenAI(
        base_url = 'http://localhost:11434/v1',
        api_key='ollama', # required, but unused
    )
    return client

# Helper function to get the output from the OpenAI model
def getOutputFromClient(client : OpenAI, messages : list):
    response = client.chat.completions.create(
        model="llama3.2",
        temperature=0.7,
        messages=messages
        )
    return response.choices[0].message.content


### ==================================================================================================
### Section 3 : Paths and filenames
### ==================================================================================================
# Paths and filenames
BASE_DIR = './files'
jobDescriptionFilename = 'jobDescription.txt'
cvFilename = 'CV.txt'

# Variables to store the content of the files and returned outputs
jobDescription = "Software Engineer"
cvContent = ""
summarizedJobDescription = ""
matchedOutput = ""
coverLetter = ""

# Variable to store the line count for the separator
lineCount = 150


### ==================================================================================================
### Section 4 : Promts for the AI model -> Begin
### ==================================================================================================

# Prompt for summarizing the job description
summarizerPrompt = """
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

# Prompt for matching skills, keywords, and relevant information
matchingSkillsPrompt = """
###
From the following job description summary:
{summarizedJobDescription}

And the following CV:
{cvContent}

Perform a hard words match between the job description summary and the CV. And list the matching skills, keywords, and relevant information.

The list should be structured as follows:
1. Matching experience: <List of matching experience>
2. Matching Skills: <List of matching skills>
3. Matching Keywords: <List of matching keywords>
4. Relevant Information: <List of relevant information>

Finally provide job title and company name.
1. Job Title: <Job Title>
2. Company Name: <Company Name>
###
"""

# Prompt for writing a cover letter
coverLetterWritingPrompt = """
###
Based on the following matched output:
{matchedOutput}

And the following CV:
{cvContent}

Write a concise and professional cover letter tailored to the highlighted information in the matched output such as <Matching experience>, <Matching Skills>, <Matching Keywords>. 
The cover letter should highlight relevant experiences, skills, and qualifications from the CV. 
It should be structured as follows:
1. Introduction: Briefly introduce yourself and state the position you are applying for.
2. Body Paragraph 1: Discuss the <List of matching experience> and how it aligns with the <List of relevant information> of the job. Avoid copying exact sentences from the CV.
3. Body Paragraph 2: Highlight the qualifications and <List of matching skills>, primarily focusing on the <List of matching keywords>.
4. Body Paragraph 3: Mention how <List of matching experience> can prove the candidate to be a perfect match for the job.
5. Conclusion: Express enthusiasm for the position.
###

---
Only include the main body in the final output and arrange the cover letter in the following way:
1. Introduction
2. Body Paragraph 1
3. Body Paragraph 2
4. Body Paragraph 3
5. Conclusion
---
"""


### ==================================================================================================
### Section 5 : Messages for the AI model -> Begin
### ==================================================================================================
summarizerMessages = [    
    {"role": "system", "content": summarizerPrompt},
    {"role": "user", "content": "Summarize the job description based on the system prompt."}
]

matchingSkillsMessages = [    
    {"role": "system", "content": matchingSkillsPrompt},
    {"role": "user", "content": "Identify and list the matching skills, keywords, and relevant information based on the system prompt."}
]

coverLetterWriterMessages = [    
    {"role": "system", "content": coverLetterWritingPrompt},
    {"role": "user", "content": "Write a cover letter based on the system prompt."}
]


### ==================================================================================================
### Section 6 : Main function
### ==================================================================================================
def main():

    global summarizerPrompt, summarizerMessages, matchingSkillsPrompt, matchingSkillsMessages, coverLetterWritingPrompt, coverLetterWriterMessages

    # Create the OpenAI client
    client = createClient()
    
    print("="*lineCount)
    print("Cover Letter Assistant")
    
    # Read the job description and CV files
    print("Reading the job description and CV files...")
    jobDescription = getFileContent(BASE_DIR, jobDescriptionFilename)
    cvContent = getFileContent(BASE_DIR, cvFilename)
    print("Files read successfully.")


    # Get the summarized job description
    summarizerPrompt = summarizerPrompt.format(jobDescription=jobDescription)
    summarizerMessages[0]["content"] = summarizerPrompt
    summarizedJobDescription = getOutputFromClient(client, summarizerMessages)
    print("Job Description Summary :")
    print("="*lineCount)
    print(summarizedJobDescription)
    print("="*lineCount)
    
    # Get the matched output
    matchingSkillsPrompt = matchingSkillsPrompt.format(summarizedJobDescription=summarizedJobDescription, cvContent=cvContent)
    matchingSkillsMessages[0]["content"] = matchingSkillsPrompt
    matchedOutput = getOutputFromClient(client, matchingSkillsMessages)
    print("Matched Output :")
    print("="*lineCount)
    print(matchedOutput)
    print("="*lineCount)

    # Get the cover letter
    coverLetterWritingPrompt = coverLetterWritingPrompt.format(matchedOutput=matchedOutput, summarizedJobDescription=summarizedJobDescription, cvContent=cvContent)
    coverLetterWriterMessages[0]["content"] = coverLetterWritingPrompt
    coverLetter = getOutputFromClient(client, coverLetterWriterMessages)
    print("Cover Letter :")
    print("="*lineCount)
    print(coverLetter, sep="\n")
    print("="*lineCount)


# main function
if __name__ == "__main__":
    main()

# **************************************** END OF CODE ****************************************