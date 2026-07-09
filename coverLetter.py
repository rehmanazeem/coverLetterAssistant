from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, AIMessagePromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama.llms import OllamaLLM
import os


class CoverLetterAssitant():
    """LangChain-based wrapper around a local Ollama model for the cover
    letter workflow (summarize job description, match CV, draft letter)."""

    def __init__(self, model_name : str, model_temperature : float = 0.6):
        """Initialize the Ollama LLM and a string output parser."""
        self.llm = OllamaLLM(model=model_name, temperature=model_temperature)
        self.output_parser = StrOutputParser()


    def getResponse(self, messages):
        """Invoke the LLM on ``messages`` and return the parsed string output."""
        response = self.llm.invoke(messages)
        return self.output_parser.parse(response)


    def getFileContent(self, path : str, filename : str):
        """Read and return the full text content of ``path/filename``."""
        with open(os.path.join(path,filename), 'r') as f:
            return f.read()


    def get_chat_prompt(self, message : list):
        """Wrap ``message`` in a LangChain ``ChatPromptTemplate``."""
        return ChatPromptTemplate([message])


    def get_job_description_summary(self, jobDescription):
        """Summarize ``jobDescription`` and return the summary plus the prompt."""
        systemMessage = """"You are an AI assitant who summarizes the job description.
        
        Your main job is to extract below mentioned important details from the job description and structure your response in the following format:
        
        Format:
        ---
        <Job Title>
        <Company Name>
        <Key responsibilities>
        <Required Qualifications>
        <Skills>
        <Important Keywords>
        <General Information>
        ---
        """

        humanMessage = "Hello! I have a job description that I would like you to summarize. Here is the job description: {job_description}"
        
        chatPrompt = self.get_chat_prompt(('system', systemMessage))
        chatPrompt.append(('human', humanMessage))

        response = self.getResponse(chatPrompt.invoke({'job_description': jobDescription}))
        chatPrompt.append(('ai', response))

        return response, chatPrompt[1:].invoke({'job_description': jobDescription})
    
    def iterate_through_conversation(self, messages):
        """Re-run the conversation through the LLM to refine the response."""
        chatPrompt = self.get_chat_prompt(
            [
            ('system', "You are an AI assistant who iterates through the conversation to get the most relevant information."),
            ('placeholder', 'conversation')
            ]
        )

        response = self.getResponse(chatPrompt.invoke({'conversation': messages}))
        chatPrompt.append(('ai', response))
        return response, chatPrompt
    
    
systemPrompt = """You are an AI assitant who drafts a cover letter based on the words, skills and keywords match from the job description and the CV of the candidate."""
summaryHumanMessage = """Here is the job description that I would like you to summarize: 
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

writerHumanMessage = """Here is the CV and the job description summary that you need to write a cover letter:

---
CV - {cv}
Job description summary - {job_description_summary}
---

Write a cover letter based on the information found in both the files. Don't forget to include only the most relevant factual information.
Avoid paraphrasing the sentences found in CV rather be creative to present the information.
Lastly, only output the body of the cover letter.
"""

BASE_DIR = './files'
jobDescriptionFilename = 'jobDescription.txt'
cvFilename = 'CV.txt'
line = "="*100

coverLetterWriter = CoverLetterAssitant(model_name='llama3.2')

jobDescription = coverLetterWriter.getFileContent(BASE_DIR, jobDescriptionFilename)
cv = coverLetterWriter.getFileContent(BASE_DIR, cvFilename)


chatPrompt = coverLetterWriter.get_chat_prompt(('system', systemPrompt))
chatPrompt.append(('human', summaryHumanMessage))
jobDescriptionSummary = coverLetterWriter.getResponse(chatPrompt.invoke({'job_description': jobDescription}))
chatPrompt.append(('ai', jobDescriptionSummary))
chatPrompt.append(('human', writerHumanMessage))


coverLetter = coverLetterWriter.getResponse(chatPrompt.invoke({'cv': cv, 'job_description_summary': jobDescriptionSummary, 'job_description': jobDescription}))

chatPrompt.append(('human', 'Take this cover letter : {cover_letter} And further optimize it to make it more matching with experience, skills and information present in the previous;y mentioned CV.'))

print(coverLetter)
print(line)

coverLetter = coverLetterWriter.getResponse(chatPrompt.invoke({'cv': cv, 
                                                               'job_description_summary': jobDescriptionSummary, 
                                                               'job_description': jobDescription, 
                                                               'cover_letter': coverLetter
                                                                }))
print(coverLetter)