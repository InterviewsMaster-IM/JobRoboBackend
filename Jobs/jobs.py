from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException, Body
from typing import List
from fastapi import Query
import motor.motor_asyncio


class Job(BaseModel):
    job_id: Optional[str] = None 
    job_board: str = Field(default="linkedin")
    company_id: str
    job_title: str = Field(..., max_length=300)
    city: str = Field(..., max_length=100)
    state: str = Field(..., max_length=100)
    is_reposted: bool
    date_posted: datetime
    n_applicants: int
    remote: str
    job_type: str
    salary: Optional[int] = None
    salary_currency: Optional[str] = None
    job_description_raw: str = Field(..., max_length=10000)

# mongoDb settings
mongo_settings = {
    "Url": "mongodb://falcon:c%23eeseP1zza@3.86.98.246:27017/",
    "database_name": "job_scrapers"
}

# post api
app = FastAPI()

# MongoDB setup (adjust with your actual settings)
client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://falcon:c%23eeseP1zza@3.86.98.246:27017')
#client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
db = client['job_scrapers']
collection = db['jobs']

@app.post("/jobs/", status_code=201)
async def create_job(jobs: List[Job]):
    try:
        # Convert each Pydantic model in the list to a dict
        jobs_dicts = [job.dict(by_alias=True) for job in jobs]
        # Insert the list of dicts into MongoDB
        await collection.insert_many(jobs_dicts)
        return {"message": "Jobs created successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
# get api
@app.get("/jobs/", response_model=List[Job])
async def read_jobs(start_date: datetime, end_date: Optional[datetime] = None, job_titles: List[str] = Query(None)):
    query = {"date_posted": {"$gte": start_date}}
    if end_date:
        query["date_posted"]["$lte"] = end_date
    if job_titles:
        query["job_title"] = {"$in": job_titles}
    jobs = await collection.find(query).to_list(None)
    return jobs
