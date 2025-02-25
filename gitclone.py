import git
import os
import shutil
import subprocess

def clone_repo_and_update_gitignore(repos_url):

    for repo in repos_url:
        if not os.path.exists('repos'):
            os.makedirs('repos')
            
        #check if the repo is already cloned
        repo_name = repo.split("https://github.com/")[1].replace('/', '-')
        if os.path.exists(f'repos/{repo_name}'):
            git.Repo(f'repos/{repo_name}').remotes.origin.pull()
        else:
            git.Repo.clone_from(repo, f'repos/{repo_name}')
    return 'repos/' + repo_name

def list_directories(folder_path):
    directories = [d for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]
    return directories


def get_branches(repo_path):
    repo = git.Repo(repo_path)
    branches = [str(branch) for branch in repo.branches]
    return branches


def run_shell_script(repo_path):
    script_path = r"..\..\trying.sh"  

    subprocess.run([script_path], cwd=repo_path, shell=True)


def main(repo_url):
    
    folder_path = 'repos'

    repos_url = []
    repos_url.append(repo_url)
    
    filename = clone_repo_and_update_gitignore(repos_url)
    #delete_folders(folder_path)
    # directories = list_directories(folder_path)
    # print("Repos to analyse", folder_path, ":", directories)

    branches = get_branches(filename)
    print("Repo  branches", branches)

    run_shell_script(filename)

    branches = get_branches(filename)
    print("Repo  branches", branches)
    
    return(filename)


#main("https://github.com/Group22-MobileApp/Grupo22-Kotlin.git")

