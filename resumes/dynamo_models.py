from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, ListAttribute, MapAttribute, NumberAttribute

class Project(MapAttribute):
    Title = UnicodeAttribute()
    Description = UnicodeAttribute()

class Education(MapAttribute):
    degree = UnicodeAttribute()
    field_of_study = UnicodeAttribute(null=True)
    college_name = UnicodeAttribute()
    country = UnicodeAttribute()
    start_date = UnicodeAttribute(null=True)
    end_date = UnicodeAttribute()
    cpa_or_percentage = UnicodeAttribute()

class WorkExperience(MapAttribute):
    job_title = UnicodeAttribute()
    is_fresher = UnicodeAttribute()
    company_name = UnicodeAttribute()
    is_current_job = UnicodeAttribute()
    work_country = UnicodeAttribute()
    start_date = UnicodeAttribute()
    end_date = UnicodeAttribute()
    work_description = UnicodeAttribute()

class Contact(MapAttribute):
    first_name = UnicodeAttribute(null=True)
    last_name = UnicodeAttribute(null=True)
    email = UnicodeAttribute(null=True)
    linkedin_url = UnicodeAttribute()
    github_url = UnicodeAttribute()
    gender = UnicodeAttribute(null=True)
    phone = UnicodeAttribute()
    date_of_birth = UnicodeAttribute(null=True)

class Skills(MapAttribute):
    hard_skills = ListAttribute(of=UnicodeAttribute)
    soft_skills = ListAttribute(of=UnicodeAttribute)

class ParsedResume(Model):
    class Meta:
        table_name = 'resumes'
        region = 'ap-south-1'
    id = UnicodeAttribute(hash_key=True)
    projects = ListAttribute(of=Project)
    Education = ListAttribute(of=Education)
    Work_Experience = ListAttribute(of=WorkExperience)
    contacts = ListAttribute(of=Contact)
    skills = Skills()
