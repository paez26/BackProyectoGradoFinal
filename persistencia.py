from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from app_secrets import ContraseñaMongoDB
from threads import milestone
from threads import issues
import numpy as np
import json
from gridfs import GridFS
from bson import ObjectId

uri= "mongodb+srv://montealegrej3:"+ContraseñaMongoDB+"@cluster.vwsy9ge.mongodb.net/?retryWrites=true&w=majority&appName=Cluster"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))


# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)


def uploadImage():
    try: 
        # Access the ProyectoDeGrado database
       

        db = client['imageP']
        
        fs = GridFS(db)

        # Open the photo file
        with open('camilocol.png', 'rb') as photo_file:
            # Store the file in GridFS
            photo_id = fs.put(photo_file, filename='photo.jpg')
        print(photo_id)
        
        
    except Exception as e :
        print(e)
    
#uploadImage()



def getImageById(id):
    try:
     
        # Access the database
        db = client['imageP']
        fs = GridFS(db)
        
        # Retrieve the image using its _id
        image = fs.get(ObjectId(id))
        
        # Save the image locally
        with open('retrieved_image.jpg', 'wb') as f:
            f.write(image.read())
        
        print("Image retrieved and saved as 'retrieved_image.jpg'")
        
    except Exception as e:
        print(e)

# imageId = "663a71f63e4bed22f3379340"
# getImageById(imageId)
    
    
def retriveInfoRepository(owner:str):
    try:
        # Access the ProyectoDeGrado database
        db = client['ProyectoDeGrado']

        # Access the repository collection
        collection = db['Repositorio']

        # Define the query
        query = {"owner": owner}

        # Retrieve the document from the collection
        document = collection.find_one(query)

        # Print the retrieved document
        print(document)
    except Exception as e:
        print(e)
        
def retrieveInfoIssues(owner:str):
    try:
        # Access the ProyectoDeGrado database
        db = client['ProyectoDeGrado']

        # Access the repository collection
        collection = db['Issues']

        # Define the query
        query = {"owner": owner}

        # Retrieve the document from the collection
        document = collection.find_one(query)

        # Print the retrieved document
        return document
    except Exception as e:
        print(e)
        
def rettrieveInfoMilestone(owner:str):
    try:
        # Access the ProyectoDeGrado database
        db = client['ProyectoDeGrado']

        # Access the repository collection
        collection = db['Milestone']

        # Define the query
        query = {"owner": owner}

        # Retrieve the document from the collection
        document = collection.find_one(query)

        # Print the retrieved document
        return document
    except Exception as e:
        print(e)
        
def retrieveUrlRepo(owner:str):
    try:
        # Access the ProyectoDeGrado database
        db = client['ProyectoDeGrado']

        # Access the repository collection
        collection = db['Repositorio']

        # Define the query
        query = {"id_repo": owner}

        # Retrieve the document from the collection
        document = collection.find_one(query)
        
   

        # Print the retrieved document
        return document["url"]
    except Exception as e:
        print(e)
        

def deleteAllData(owner:str):
    try:
        # Access the ProyectoDeGrado database
        db = client['ProyectoDeGrado']

        # Access the repository collection
        collection = db['Repositorio']

        # Define the query
        query = {"id_repo": owner}

        # Retrieve the document from the collection
        collection.delete_one(query)
        
        # Access the repository collection
        collection = db['Issues']

        # Define the query
        query = {"owner": owner}

        # Retrieve the document from the collection
        collection.delete_one(query)
        
        # Access the repository collection
        collection = db['Milestone']

        # Define the query
        query = {"owner": owner}

        # Retrieve the document from the collection
        collection.delete_one(query)
        
        # Access the repository collection
        collection = db['Allrepository']

        # Define the query
        query = {"owner": owner}

        # Retrieve the document from the collection
        collection.delete_one(query)
        
    except Exception as e:
        print(e)
        

    
        

def addInfoRepository(repoInfo:dict, owner:dict):
    try:
        
        
        

        # Access the ProyectoDeGrado database
        db = client['ProyectoDeGrado']

        # Access the repository collection
        collection = db['Repositorio']

        # Define the new document
        document = {
  
        }
        for key in repoInfo:
            document[key] = repoInfo[key]

        
        # Insert the new document into the collection
        collection.insert_one(document)

        # Print the inserted document

        
    except Exception as e:
        print(e)



def checkIfRepoExists(repoName:str): 
    try:
        # Access the ProyectoDeGrado database
        db = client['ProyectoDeGrado']

        # Access the repository collection
        collection = db['generalData']

        # Define the query
        query = {"owner": "PGCJD"}

        # Retrieve the document from the collection
        document = collection.find_one(query)

        listas= document["ListaRepos"]
        
        if repoName in listas:
            return True
        else:
            return False
        
    except Exception as e:
        print(e)
        

def addRepoToListGeneralData(repoName:str):
    try:
        # Access the ProyectoDeGrado database
        db = client['ProyectoDeGrado']

        # Access the repository collection
        collection = db['generalData']

        # Define the query
        query = {"owner": "PGCJD"}
        
        # Retrieve the document from the collection
        document = collection.find_one(query)
        
        listas= document["ListaRepos"]
        
        listas.append(repoName)
        
        collection.update_one(query, {"$set": {"ListaRepos": listas}})
        
    
    except Exception as e:
        print(e)
        
        
        
def startThreads(RepoName:str, urlApi:str):
    buscador_milestone = milestone.Milestone(urlApi, RepoName)
    buscador_milestone.start()
    buscador_issues = issues.Issue(urlApi, RepoName)
    buscador_issues.start()
    
    buscador_milestone.join()
    buscador_issues.join()
    
    dicMilestone = buscador_milestone.dic
    dicIssues = buscador_issues.resutl_issues
    totalMil = buscador_milestone.total_milestones
    totalIss = buscador_issues.total_issues_count
    
    # print(dicMilestone)
    # print(dicIssues)
    # print(totalMil)
    # print(totalIss)
    
    try:
        # Access the ProyectoDeGrado database
        db = client['ProyectoDeGrado']

        # Access the repository collection
        collection = db['Repositorio']

        # Define the query
        query = {"id_repo": RepoName}
        
        # Retrieve the document from the collection
        document = collection.find_one(query)
        
        document["lastMilestone"] = totalMil
        document["lastIssue"] = totalIss
        
        collection.update_one(query, {"$set":  {"lastIssue": totalIss}})
        collection.update_one(query, {"$set":  {"lastMilestone": totalMil}})
    
    
    except Exception as e:
        print(e)
        
    try:
    
        # Access the ProyectoDeGrado database
        db = client['ProyectoDeGrado']

        # Access the repository collection
        collection = db['Issues']
        
        # Insert the new document into the collection
        collection.insert_one(dicIssues)

    except Exception as e:
        print(e)
        
    try:
    
        # Access the ProyectoDeGrado database
        db = client['ProyectoDeGrado']

        # Access the repository collection
        collection = db['Milestone']
        
        # Insert the new document into the collection
        collection.insert_one(dicMilestone)

    except Exception as e:
        print(e)
        
        
def getAllRepositories():
    try:
        # Access the ProyectoDeGrado database
        db = client['ProyectoDeGrado']

        # Access the repository collection
        collection = db['generalData']

        # Define the query
        query = {"owner": "PGCJD"}

        # Retrieve the document from the collection
        document = collection.find_one(query)

        listas= document["ListaRepos"]
        
        return listas
        
    except Exception as e:
        print(e)
        
def updateRepoInfo(info:str):
    owner = info["id_repo"]
    try:
        # Access the ProyectoDeGrado database
        db = client['ProyectoDeGrado']

        # Access the repository collection
        collection = db['Repositorio']

        # Define the query
        query = {"id_repo": owner}
        
        # Retrieve the document from the collection
        document = collection.find_one(query)
        
        for key in info:
            document[key] = info[key]
        
        collection.update_one(query, {"$set": document})
    except Exception as e:
        print(e)
        
        
def pushDriller(repoInfo: dict, owner: str):
    
    try:
        # Access the ProyectoDeGrado database
        db = client['ProyectoDeGrado']

        # Access the repository collection
        collection = db['Allrepository']
        # Insert the new document into the collection
        #repoInfo["owner"] = owner
        collection.insert_one(json.loads(repoInfo))

    except Exception as e:
        print("Error:", e)

def pushTestLog(nameInfo: str):
    
    try:
        # Access the ProyectoDeGrado database
        db = client['ProyectoDeGrado']

        tests = {}
        tests['owner'] =  nameInfo
        tests['testsLogs'] = []
        tests['youtube'] = []

        def convert(obj):
                    if isinstance(obj, np.int64):
                            return int(obj)
                    return obj

        final = json.dumps(tests, default=convert)

        # Access the repository collection
        collection = db['AllTests']
        # Insert the new document into the collection
        #repoInfo["owner"] = owner
        collection.insert_one(json.loads(final))

    except Exception as e:
        print("Error:", e)

def addYoutube(youtubeId:str, nameInfo: str):
    
    try:
        # Access the ProyectoDeGrado database
        db = client['ProyectoDeGrado']
        # Access the repository collection
        collection = db['AllTests']

        query = {"owner": nameInfo}
        
        # Retrieve the document from the collection
        document = collection.find_one(query)
        
        
        collection.update_one(query, {"$push":  {"youtube": youtubeId}})
        # Insert the new document into the collection
        #repoInfo["owner"] = owner
        #collection.update_one(json.loads(final))

    except Exception as e:
        print("Error:", e)

def addTestLog(testLoginfo:str, nameInfo: str):
    
    try:
        # Access the ProyectoDeGrado database
        db = client['ProyectoDeGrado']
        # Access the repository collection
        collection = db['AllTests']

        query = {"owner": nameInfo}
        
        # Retrieve the document from the collection
        document = collection.find_one(query)
        
        
        collection.update_one(query, {"$push":  {"testsLogs": testLoginfo}})
        # Insert the new document into the collection
        #repoInfo["owner"] = owner
        #collection.update_one(json.loads(final))

    except Exception as e:
        print("Error:", e)

def getTestsLog(owner):
    try:
        # Access the ProyectoDeGrado database
        db = client['ProyectoDeGrado']

        # Access the repository collection
        collection = db['AllTests']

        # Define the query
        query = {"owner": owner}

        # Retrieve the document from the collection
        document = collection.find_one(query)

        # Print the retrieved document
        return document
    except Exception as e:
        print(e)

def getReposAnalysis():
    try:
        # Access the ProyectoDeGrado database
        db = client['ProyectoDeGrado']

        # Access the repository collection
        collection = db['generalData']

        # Define the query
        query = {"owner": "PGCJD"}

        # Retrieve the document from the collection
        document = collection.find_one(query)

        # Print the retrieved document
        return document.ListaRepos
    except Exception as e:
        print(e)     

def getRepoEquipo(owner):
    try:
        # Access the ProyectoDeGrado database
        db = client['ProyectoDeGrado']

        # Access the repository collection
        collection = db['Allrepository']

        # Define the query
        query = {"owner": owner}

        # Retrieve the document from the collection
        document = collection.find_one(query)

        # Print the retrieved document
        return document
    except Exception as e:
        print(e)
        

def getInfoRepoEquipo(owner):
    try:
        # Access the ProyectoDeGrado database
        db = client['ProyectoDeGrado']

        # Access the repository collection
        collection = db['Repositorio']

        # Define the query
        query = {"id_repo": owner}

        # Retrieve the document from the collection
        document = collection.find_one(query)

        # Print the retrieved document
        return document
    except Exception as e:
        print(e)
    
    
        
# def pushinfo():
    
#     try:
#         # Access the ProyectoDeGrado database
#         db = client['ProyectoDeGrado']

#         # Access the repository collection
#         collection = db['Allrepository']

#         dic = {'camilolcoder': {'num_inserts': 1333, 'num_deletes': 189, 'net_lines': 1144, 'files': {'ic_launcher_round.webp': 5, 'ic_launcher_foreground.webp': 5, 'ic_launcher.webp': 5, 'DetailsNavGraph.kt': 5, 'MainHomeContent.kt': 4}, 'commits': 18, 'avg_lines': 63.55555555555556, 'inserts': {'2024-03': 22, '2024-04': 1311}}, 'montejs3': {'num_inserts': 7657, 'num_deletes': 518, 'net_lines': 7139, 'files': {'build.gradle.kts': 14, 'LoginContent.kt': 12, 'LoginScreen.kt': 9, 'AppModule.kt': 8, 'LoginViewModel.kt': 7}, 'commits': 29, 'avg_lines': 246.17241379310346, 'inserts': {'2024-03': 7657}}, 'dcgonzalezp': {'num_inserts': 4811, 'num_deletes': 1179, 'net_lines': 3632, 'files': {'AddPostContent.kt': 6, 'DefaultTextField.kt': 6, 'ProfileImage.kt': 5, 'LoginContent.kt': 4, 'ProfileContent.kt': 4}, 'commits': 26, 'avg_lines': 139.69230769230768, 'inserts': {'2024-03': 4490, '2024-04': 321}}, 'Camilo Colmenares': {'num_inserts': 3198, 'num_deletes': 695, 'net_lines': 2503, 'files': {'AddPostViewModel.kt': 10, 'AddPostContent.kt': 8, 'PostRepositoryImpl.kt': 6, 'PostRepository.kt': 5, 'PostViewModel.kt': 4}, 'commits': 27, 'avg_lines': 92.70370370370371, 'inserts': {'2024-03': 2985, '2024-04': 213}}}
#         # Insert the new document into the collection
#         collection.insert_one(dic)

#     except Exception as e:
#         print("Error:", e)

# pushinfo()


#startThreads("INFO-ISIS3510-202320-Team31Android-Kotlin", "https://api.github.com/repos/ISIS3510-202320-Team31/Android-Kotlin")