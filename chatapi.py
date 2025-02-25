import openai
from openai import OpenAI
import os
from app_secrets import APICHAT
client = OpenAI(
   api_key=APICHAT)


completion = client.chat.completions.create(
  model="gpt-3.5-turbo-16k",
  messages=[
    {"role": "system", "content": "You are a teaching assistant assistant that write the anseer in json, doa false true question about a code ."},
    {"role": "user", "content": "@app.post('/createRepo/')async def create_item(repo: Repo):print('Buscando estadisticas de: '+ str(repo.url))info = checkIfRepoIsInDataBase(str(repo.url))return info"}
  ]
)

print(completion.choices[0].message)