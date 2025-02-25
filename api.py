from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from modelo import checkIfRepoIsInDataBase
from modelo import getUrlRepo
from persistencia import getAllRepositories
from persistencia import getRepoEquipo
from persistencia import getInfoRepoEquipo
from persistencia import retrieveInfoIssues
from persistencia import rettrieveInfoMilestone
from persistencia import retrieveUrlRepo
from persistencia import getTestsLog 
from modelo import getApiRepo
from modelo import run_youtube
from testing import start_monkey_testing
from joblib import load
import pandas as pd
import io
import joblib
import numpy as np
import pandas as pd
import requests
from app_secrets import TOKENgithub
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import (
    ConfusionMatrixDisplay, RocCurveDisplay,
    roc_auc_score, precision_score, recall_score, f1_score
)
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.pipeline import Pipeline


# To run uvicorn api:app --reload
app = FastAPI()

allowed_origins = [
    "http://localhost:3000",
]

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
       
def convert_objectid(document):
    if isinstance(document, dict):
        for key, value in document.items():
            if isinstance(value, ObjectId):
                document[key] = str(value)
            elif isinstance(value, dict):
                document[key] = convert_objectid(value)
            elif isinstance(value, list):
                document[key] = [convert_objectid(item) if isinstance(item, (dict, list)) else item for item in value]
    elif isinstance(document, list):
        document = [convert_objectid(item) if isinstance(item, (dict, list)) else item for item in document]
    return document
    

class Repo(BaseModel):
    url: str

class Test(BaseModel):
    url:str
    package:str
    inputs:str
    
    
class DataModel(BaseModel):
    texto: str
    


@app.post("/createRepo/")
async def create_item(repo: Repo):
    print("Buscando estadisticas de: "+ str(repo.url))
    info = checkIfRepoIsInDataBase(str(repo.url))
    return info

@app.post("/createTest/")
async def create_test(repo: Test):
    print("Realizando pruebas a: "+ str(repo.url))
    info = start_monkey_testing(repo.url, repo.package, repo.inputs)
    return info

@app.get("/createYoutube/")
def create_test(url: str):
    print("Subiendo video a youtube")
    info = run_youtube(url)
    return info

@app.get("/createget")
def create_item(repo: str):
    print("Buscando estadisticas de: "+ str(repo))
    info = checkIfRepoIsInDataBase(str(repo))
    return info

@app.get("/predict")
def make_predictions(dataModel: str):
    mesage= dataModel
    df = pd.DataFrame()
    df['msg'] = [mesage]
    model = load('pipe.joblib')
    df['sdg'] = model.predict(df["msg"])
    p= df.to_dict(orient="records")
    print(p[0])
    
    return p[0]

@app.get("/getRepos")
def getRepos():
    repos = getAllRepositories()
    return repos

@app.get("/getInfoEquipo")
def getInfoEquipo(url: str):
   # print(url)
    document = getRepoEquipo(url) #it comes from a document in mongo db
    del document['_id'] 
    del document['owner']
  #  print(document)
    return document

@app.get("/getTestLog")
def getRepoInfo(url: str):
    document = getTestsLog(url)
    del document['_id']
    return document

@app.get("/getRepoInfo")
def getRepoInfo(url: str):
    document =getInfoRepoEquipo(url)
    del document['_id']
    return document

@app.get("/getRepoIssues")
def getRepoIssues(url: str):
    document = retrieveInfoIssues(url)
    document = convert_objectid(document)
    return document

@app.get("/getRepoMilestone")
def getRepoMilestone(url: str):
    document = rettrieveInfoMilestone(url)
    document = convert_objectid(document)
    return document

@app.get("/getRepoOpenIssues")
def getRepoOpenIssues(url: str):
    urldefinitiva = retrieveUrlRepo(url)
    print(urldefinitiva)
    api_url = getUrlRepo(urldefinitiva)
    token = TOKENgithub
    headers = {"Authorization": "Bearer " + token}
    api_url= api_url + "/issues"
    try:
        # Make a GET request to the GitHub API
        response = requests.get(api_url, headers=headers)
        
        # If the response was successful, no Exception will be raised
    except Exception as e:
        # Handle the exception here
        print(e)
    
    return response.json()
