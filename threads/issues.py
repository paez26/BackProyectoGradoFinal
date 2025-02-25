
import threading
import time
import requests
import json
import logging
from app_secrets import TOKENgithub

logging.basicConfig(level=logging.INFO)
class Issue(threading.Thread):
    def __init__(self, url, name_file):
        super().__init__()
        self.url = url
        self.name_file = name_file
        self.total_issues_count = 0
        self.resutl_issues = {}
        
    def result(self):
        return self.resutl_issues
        
    def run(self):
        token = TOKENgithub
        headers = {"Authorization": "Bearer " + token}
        total_issues = 0
        issues_closed = 0
        issues_open = 0
        contador = 1
        lista_issues = []
        centinela = True
        info_issues = {}
        while centinela and contador < 24: 
           
            dic_issues = {}
            logging.info(f"Analyzing Issue page: {contador}")
            api_url = f"{self.url}/issues/{contador}"
            #print(api_url)
            try:
                response = requests.get(api_url, headers=headers)
                response_json = response.json()
                if "message" in response_json and response_json["message"] == "Not Found":
                    logging.info("No more issues")
                    centinela = False
                    break
                dic_issues["title"] = response_json.get("title", "")
                dic_issues["state"] = response_json.get("state", "")
                dic_issues["created_at"] = response_json.get("created_at", "")
                dic_issues["url"] = response_json.get("url", "")
                
                dic_issues["assignee"] = response_json.get("assignee", "")
                dic_issues["closed_by"] = response_json.get("assignee", {"login": "Null"})
                if response_json.get("state", "") == "open":
                    issues_open += 1
                else:
                    issues_closed += 1
                total_issues += 1
              
                lista_issues.append(dic_issues)
                time.sleep(10)
            except requests.exceptions.RequestException as e:
                logging.error(f"Error occurred during request: {e}")
                break
            except json.JSONDecodeError as e:
                logging.error(f"Error decoding JSON: {e}")
                break
            contador += 1
        
        info_issues["totalIssues"] = total_issues
        info_issues["issuesClosed"] = issues_closed
        info_issues["issuesOpen"] = issues_open
        info_issues["owner"] = self.name_file
        info_issues["issues"] = lista_issues
        
        self.resutl_issues = info_issues
        self.total_issues_count = total_issues
        #print(lista_issues)
        return info_issues

# # Example usage
# url = "https://api.github.com/repos/Group22-MobileApp/Grupo22-Kotlin"
# name_file = "example"
# issue_thread = Issue(url, name_file)
# issue_thread.start()
# issue_thread.join()  # Wait for the thread to finish

        
        
                
       
        
   