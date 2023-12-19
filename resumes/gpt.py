from openai import OpenAI
from django.conf import settings
import json


PROMPT="""
You are a resume parser who helps user in extracting information of candidates.
User will give the text extracted from the resume of a candidate.
Output the data in the given syntax in json format:
{
    "projects": [
        {"Title": "project_1_title", "Description": "project_1_description"},
        # Add more project entries as needed for project_2_title, project_3_title ....... if available 
    ]
    ,
    "Education": [
        {degree: "degree_1", field_of_study: "field_of_study_1", college_name: "college_name_1", country: "country_1", start_date: "start_date_1", end_date: "end_date_1", cpa_or_percentage: "cpa_or_percentage_1"},
        .........
        # Add more education entries as needed for degree_2, degree_3....... if available 
    ],
    "Work_Experience": [
        {job_title: "job_title_1", is_fresher: "True or False", company_name: "company_name_1", is_current_job: "True or False", work_country: "work_country_1", start_date: "start_date_1", end_date: "end_date_1", work_description: "work_description_1"},
        ............
        # Add more work experience entries as needed for job_title_2, job_title_3....... if available
    ],
    "contacts": [
        {first_name: "first_name", last_name: "last_name", email: "email", linkedin_url: "linkedin_url", github_url: "github_url", gender: "gender", phone: "phone_number", date_of_birth: "date_of_birth"}
    ],
    "skills": 
        {
            "hard_skills": ["hard_skills_1", "hard_skills_2", "hard_skills_3", ...],
            "soft_skills": ["soft_skills_1", "soft_skills_2", "soft_skills_3", ...]
        }
}

If information is not found in the resume text, use "" in the response for that field.
"""



class GPTAgent:


    def __init__(
        self, temperature=0.0, messages=None,top_p=0.5
    ):
        
        # "gpt-4-1106-preview" for gpt-4
        self.client = OpenAI(api_key=settings.OPEN_AI_KEY)        
        self.prompt = PROMPT
        self.messages = messages or []
        self.messages.append(
            self.create_chat_message(role="system", content=self.prompt)
        )
        self.model = settings.OPEN_AI_MODEL
        self.temperature = temperature
        self.top_p=top_p


    def create_chat_message(self, role, content):
        return {"role": role, "content": content}


    def get_assistant_message(self):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=self.temperature,
            top_p=self.top_p,
            response_format={"type":"json_object"}
        )        
        self.add_message(response.choices[0].message.content,role="system")
        return json.loads(response.choices[0].message.content)
    

    def add_message(self, content, role="user"):
        msg = self.create_chat_message(role, content)
        self.messages.append(msg)

    def print_message_history(self):
        for msg in self.messages:
            print(f"{msg['role']}: { msg['content']} ")
            print(
                "------------------------------------------------------------------------"
            )

