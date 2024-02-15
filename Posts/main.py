import os
from fastapi import FastAPI, HTTPException,Body,Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

app = FastAPI()
load_dotenv()
mongo_uri = os.getenv("MONGO_URI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# mongo_client = MongoClient(mongo_uri)
mongo_client = MongoClient('mongodb://falcon:c%23eeseP1zza@3.86.98.246/?authMechanism=DEFAULT&authSource=admin')
db = mongo_client["job_scrapers"]

# Get Latest Profiles {name,url}
@app.get("/profiles")
async def get_profiles_list(limit: int = Query(10, title="Number of Documents", description="Specify the number of documents needed")):
    try:
        collection = db["linkedin_only_post_test"]

        # Fetch all documents from the collection
        documents = collection.find({}, {"authorName": 1, "authorUrl": 1, "_id": 0}).sort([("createdAt", -1)]).limit(limit)

        # Extract authorName and authorUrl from each document
        authors = [{"profileName": doc["authorName"], "profileUrl": doc["authorUrl"]} for doc in documents]

        return authors
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/insert_data")
async def insert_data(request_data: list = Body(...)):
    try:
        collection = request_data[0]["collection"]
        data = request_data[0]["data"]

        # Generate new ObjectId
        data["_id"] = ObjectId()

        # Set createdAt and updatedAt to the current server time
        current_time = datetime.utcnow()
        data["createdAt"] = current_time
        data["updatedAt"] = current_time

        # Insert the document into MongoDB
        db[collection].insert_one(data)

        return JSONResponse(content={"message": f"Document inserted successfully into {collection}"}, status_code=201)
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Route to check if a key-value pair exists in the collection
@app.post("/check_unique")
async def check_unique(data: dict = Body(...)):
    try:
        # Validate required parameters
        required_params = ["collection", "key", "value"]
        for param in required_params:
            if param not in data:
                return JSONResponse(content={"message": f"Missing required parameter: {param}"}, status_code=400)

        # Extract parameters from the request body
        collection_name = data["collection"]
        key = data["key"]
        value = data["value"]

        # Check if the key-value pair exists in the specified collection
        existing_document = mongo_client[db.name][collection_name].find_one({key: value})

        return {"isExists": existing_document is not None}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=180)