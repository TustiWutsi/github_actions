from fastapi import FastAPI, HTTPException, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import base64
from pydantic import BaseModel, constr
from typing import Optional, List, Literal
import pandas as pd

questions = pd.read_csv('questions.csv')

app = FastAPI()

# allowed credentials
user_credentials = {
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine"
}

def authenticate(request: Request):
    # get Authorization headers
    authorization: str = request.headers.get("Authorization")

    # Check if it starts by "Basic "
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    elif not authorization.startswith("Basic "):
        raise HTTPException(status_code=401, detail="Authorization header malformed : must start by 'Basic '")

    # Get base64 information
    credentials_base64 = authorization[len("Basic "):]
    
    try:
        # Decode base64 information
        credentials = base64.b64decode(credentials_base64).decode("utf-8")
        username, password = credentials.split(":", 1)
    except (ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    
    # Check if they match with allowed credentials
    if username not in user_credentials.keys() or user_credentials[username] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

class Criteria(BaseModel):
    test_type: Literal["Test de validation", "Test de positionnement", "Total Bootcamp"]
    categories: List[Literal["BDD", "Systèmes distribués", "Streaming de données", "Docker", "Classification", "Data Science", "Machine Learning", "Automation"]]
    number_of_questions: Literal[5, 10, 20]

class CriteriaAdmin(BaseModel):
    admin_username: Literal["admin"]
    admin_password: Literal["4dm1N"]
    question: str
    subject: Literal["BDD", "Systèmes distribués", "Streaming de données", "Docker", "Classification", "Data Science", "Machine Learning", "Automation"]
    correct: List[str]
    use: Literal["Test de validation", "Test de positionnement", "Total Bootcamp"]
    responseA: constr(min_length=1)
    responseB: constr(min_length=1)
    responseC: Optional[str] = None
    responseD: Optional[str] = None

@app.get('/verify')
def verify():
    return {
        "message": "L'API est fonctionnelle."
        }

@app.post('/generate_quiz')
def generate_quiz(criteria: Criteria, request: Request):

    authenticate(request)

    try:
        filtered_questions = questions[(questions['subject'].isin(criteria.categories))&(questions['use'] == criteria.test_type)]

        if len(filtered_questions) < criteria.number_of_questions:
            raise HTTPException(status_code=400, detail="Not enough questions available for the requested quiz")

        final_questions = filtered_questions.sample(criteria.number_of_questions).fillna("")
        final_questions_dict = final_questions.to_dict(orient="records")

        return final_questions_dict
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post('/create_question')
def create_question(criteria_admin: CriteriaAdmin):
    return {"message": "Question créée avec succès."}