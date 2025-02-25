import threading
import time
import requests
import json
import logging
from app_secrets import TOKENgithub

logging.basicConfig(level=logging.INFO)

class Milestone(threading.Thread):
    def __init__(self, url, name_file):
        super().__init__()
        self.url = url
        self.name_file = name_file
        self.dic= {}
        self.total_milestones = 0
        
    def result(self):
        return self.dic
        
    def run(self):
        token = TOKENgithub
        headers = {"Authorization": "Bearer " + token}
        total_milestones = 0
        contador = 1
        milestone_dict = {}
        milestone_list = []

        while contador < 10: 
            dic_milestone = {}
            logging.info(f"Analyzing milestone page: {contador}")
            api_url = f"{self.url}/milestones/{contador}"
            
            try:
                response = requests.get(api_url, headers=headers)
                response_json = response.json()
             
                # print(response_json)
                if "message" in response_json and response_json["message"] == "Not Found":
                    logging.info("No more milestones")
                    
                    break
                
                dic_milestone["title"] = response_json.get("title", "")
                dic_milestone["description"] = response_json.get("description", "")
                dic_milestone["creator"] = response_json.get("creator", {}).get("login", "")
                dic_milestone["open_issues"] = response_json.get("open_issues", 0)
                dic_milestone["closed_issues"] = response_json.get("closed_issues", 0)
                dic_milestone["created_at"] = response_json.get("created_at", "")
                dic_milestone["closed_at"] = response_json.get("closed_at", "")
                dic_milestone["state"] = response_json.get("state", "")
                
                total_milestones += 1
                contador += 1
                milestone_list.append(dic_milestone)
                time.sleep(10)
            except requests.exceptions.RequestException as e:
                logging.error(f"Error occurred during request: {e}")
                break
            except json.JSONDecodeError as e:
                logging.error(f"Error decoding JSON: {e}")
                break
            
        milestone_dict["owner"] =  self.name_file 
        milestone_dict["totalMilestones"] = total_milestones
        milestone_dict["milestones"] = milestone_list
        #print(milestone_dict)
        self.dic = milestone_dict
        self.total_milestones = total_milestones
        return milestone_dict

# # Example usage
# url = "https://api.github.com/repos/ISIS3510-202320-Team31/Android-Kotlin"
# name_file = "example"
# milestone_thread = Milestone(url, name_file)
# milestone_thread.start()
# milestone_thread.join()  # Wait for the thread to finish


            
            
                
            