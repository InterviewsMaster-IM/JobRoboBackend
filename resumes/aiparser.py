import PyPDF2
from .gpt import GPTAgent
from .models import Resume
from .dynamo_models import *
from celery import shared_task


def extract_text_from_pdf(file_obj):
    reader = PyPDF2.PdfReader(file_obj)
    text = ""
    for page_num in range(len(reader.pages)):
        text += reader.pages[page_num].extract_text()
    return text

def parse_resume_text(resume_text):
    agent = GPTAgent();
    agent.add_message(resume_text)
    response = agent.get_assistant_message()
    return response

def parse_resume_save_in_db(resume):
    file = resume.file
    text = extract_text_from_pdf(file)
    data = parse_resume_text(text)
    # print(data)
    
    #populate data in dynamodb model    
    parsed_resume = ParsedResume()
    parsed_resume.id = str(resume.user)+"_"+str(resume.id)
    parsed_resume.projects = [Project(**project) for project in data['projects']]
    parsed_resume.Education = [Education(**education) for education in data['Education']]
    parsed_resume.Work_Experience = [WorkExperience(**work_exp) for work_exp in data['Work_Experience']]
    parsed_resume.contacts = [Contact(**contact) for contact in data['contacts']]
    parsed_resume.skills = Skills(hard_skills=data['skills']['hard_skills'], soft_skills=data['skills']['soft_skills'])
    parsed_resume.save()

@shared_task
def parse_resume_save_in_db_task(resume_id):
    resume = Resume.objects.get(id=resume_id)
    parse_resume_save_in_db(resume)
