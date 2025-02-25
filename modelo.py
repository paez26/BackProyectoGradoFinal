import os
import json
import requests
from app_secrets import TOKENgithub
from persistencia import addInfoRepository
from persistencia import checkIfRepoExists
from persistencia import addRepoToListGeneralData
from persistencia import startThreads
from persistencia import pushDriller
from persistencia import pushTestLog
from persistencia import updateRepoInfo
from persistencia import deleteAllData
from driller import pydriller
from youtube_script import initialize_upload
from youtube_script import get_authenticated_service



def getApiRepo(url):
    name = url.replace(".git", "")
    name = name.split("/")
    owner = name[-2]
    repo_name = name[-1]
    api_url = f"https://api.github.com/repos/{owner}/{repo_name}"
    print(api_url)
    nameinfo= "INFO-" + owner + '-' + repo_name 
    return api_url, nameinfo

def getUrlRepo(nameinfo:str):
    name = nameinfo.split("/")
    owner = name[-2]
    repo_name = name[-1]
    api_url = f"https://api.github.com/repos/{owner}/{repo_name}"
    return api_url
    




def getInfoGeneral(api_url,nameinfo):
    
    # github token for authentication in the API
    token = TOKENgithub
    headers = {"Authorization": "Bearer " + token}
    repoInfo= {}
    try:
        # Make a GET request to the GitHub API
        response = requests.get(api_url, headers=headers)
        
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except Exception as e:
        # Handle the exception here
        print(e)
        
    try:
        # Make a GET request to the GitHub API to get the branches
        branchs = requests.get(api_url+"/branches", headers=headers)
        branchs = branchs.json()
        contadorbranchs=0
        for branch in branchs:
            contadorbranchs+=1
        
    except Exception as e:
        # Handle the exception here
        print(e)
        
   
        
    response = response.json()
    repoInfo["id_repo"] = nameinfo
    repoInfo["avatar_url"]= response["owner"]["avatar_url"]  #Nuevooooo
    repoInfo["name"]= response["name"]
    repoInfo["url"] = response["html_url"]
    repoInfo["visibility"]= str(response["visibility"])
    repoInfo["owner"] = response["owner"]["login"]
    repoInfo["language"] = response["language"]
    repoInfo["open_issues_count"] = response["open_issues_count"] #Nuevooooo
    repoInfo["watchers_count"] = response["watchers_count"]       #Nuevooooo
    repoInfo["created_at"] = response["created_at"]
    repoInfo["updated_at"] = response["updated_at"]
    repoInfo["pushed_at"] = response["pushed_at"]
    repoInfo["is_template"] = str(response["is_template"])       #Nuevooooo
    repoInfo["Branchs"] = contadorbranchs
    repoInfo["last_commit"] = ""
    repoInfo["lastMilestone"] = ""
    repoInfo["lastIssue"] = ""
   
    
    
    
    return repoInfo 




def checkIfRepoIsInDataBase(url:str):
    api_url, nameinfo = getApiRepo(url)
    
    inDataBase= checkIfRepoExists(nameinfo)
    
    if inDataBase:
        deleteAllData(nameinfo)
        RepoInfo = getInfoGeneral(api_url,nameinfo)
        addInfoRepository(RepoInfo, nameinfo)
        startThreads(nameinfo,api_url)
        
        dicdriller, repodriller=pydriller(url,nameinfo)
        pushDriller(dicdriller, nameinfo)
        pushTestLog(nameinfo)

        updateRepoInfo(repodriller)
        return "Repositorio agregado exitosamente"
    else:
        
        RepoInfo = getInfoGeneral(api_url,nameinfo)
        addInfoRepository(RepoInfo, nameinfo)
        addRepoToListGeneralData(nameinfo)
        
        startThreads(nameinfo,api_url)
        
        dicdriller, repodriller=pydriller(url,nameinfo)
        pushDriller(dicdriller, nameinfo)
        pushTestLog(nameinfo)

        updateRepoInfo(repodriller)
        return "Repositorio agregado exitosamente"
     
def run_youtube(url:str):
    youtube = get_authenticated_service()
    try:
        initialize_upload(youtube, 'screenrecord2.mp4', url)
        #return "Success"
    except Exception as e:
        print(f'An error occurred: {e}')
        #return "Failed"
        
    
    
    
    
        
        
        
        
    

    
    
    
    
    





