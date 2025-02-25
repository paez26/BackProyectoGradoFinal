import git
import os
import shutil
import subprocess
import time
import numpy as np
import asyncio
import json
from pyppeteer import launch
from persistencia import pushTestLog
from persistencia import addTestLog

def clone_repo_and_update_gitignore(repos_url):

    for repo in repos_url:
        repo_name = repo.split("https://github.com/")[1].replace('/', '-')
        git.Repo.clone_from(repo, f'repos/{repo_name}')

def list_directories(folder_path):
    directories = [d for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]
    return directories

#This one gives me an error due to permissions :( but it doesn't matter
def delete_folders(folder_path):
    repos = os.listdir(folder_path)
    
    for repo in repos:
        repo_path = os.path.join(folder_path, repo)
        
        if os.path.isdir(repo_path):
            shutil.rmtree(repo_path)

def get_branches(repo_path):
    repo = git.Repo(repo_path)
    branches = [str(branch) for branch in repo.branches]
    return branches

def git_checkout(repo_path, branch_name):
    repo = git.Repo(repo_path)
    repo.git.checkout(branch_name)


def fetch_all_branches(repo_path):
    repo = git.Repo(repo_path)

    origin = repo.remote(name='origin')
    origin.fetch()

    for remote_ref in origin.refs:
        branch_name = remote_ref.remote_head.split('/')[-1]
        repo.git.checkout('-t', remote_ref, b=branch_name)

def run_shell_script(repo_path):
    script_path = r"..\..\trying.sh"  

    subprocess.run([script_path], cwd=repo_path, shell=True)

def start_emulator(avd_name):
    emulator_command = f"emulator -avd {avd_name}"
    subprocess.Popen(emulator_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def build_debug_apk(repo_path):
    #subprocess.run(["cd", repo_path], shell=True)
    subprocess.run([".\gradlew.bat", "assembleDebug"], cwd=repo_path, shell=True)


def install_apk(apk_path):
    command = ["adb", "install", "-r", apk_path]
    subprocess.run(command)

def run_monkey_test(package, inputs, output_file):
    command = ["adb", "shell", "monkey", "-p", package, "-v", inputs] #, "|", "tee", package+".txt"]
    subprocess.run(command)

    with open(output_file, "w") as f:
        subprocess.run(command, stdout=f, stderr=subprocess.STDOUT)

def start_screen_record(output_file): #duractio  '--time-limit',
    subprocess.Popen(['adb', 'shell', 'screenrecord', output_file], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def stop_screen_record():
    #subprocess.run(['adb', 'shell', 'pkill', '-l', '15', 'screenrecord'])
    #subprocess.run(['adb', 'shell', 'killall', '-2', 'screenrecord'])
    pid_output = subprocess.check_output(['adb', 'shell', 'pidof', 'screenrecord'])
    pid = pid_output.decode('utf-8').strip()
    subprocess.run(['adb', 'shell', 'kill', '-2', pid])

def npm_install(repo_path):
    subprocess.run(["npm", "install"], cwd=repo_path, shell=True)

def start_project_front(repo_path):
    subprocess.run(["npm", "start"], cwd=repo_path, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def start_project_back(repo_path):
    subprocess.run(["npm", "run", "start:dev"], cwd=repo_path, shell=True) 

def monkey_web_test(repo_path):
    #subprocess.run(["cd", repo_path], shell=True)
    subprocess.run(["npm", "install"], cwd=repo_path, shell=True)

async def run_gremlins_test(url):
    browser = await launch()
    page = await browser.newPage()

    try:
        await page.goto(url)

        await page.addScriptTag({'url': 'https://cdn.jsdelivr.net/npm/gremlins.js@gremlins.min.js'})

        await page.evaluate('''() => {
            const horde = window.gremlins.createHorde();
            horde.seed(1234); // Set a seed for reproducible tests
            horde.unleash();
        }''')

        await asyncio.sleep(5)

    finally:
        await browser.close()


def get_screen_record(path_record):
    subprocess.run(['adb', 'pull', path_record])


def parse_file_to_dict(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # tests = {}
    # tests['owner'] =  repo_name
    # tests['testsLogs'] = [content]

    # def convert(obj):
    #             if isinstance(obj, np.int64):
    #                     return int(obj)
    #             return obj

    # final = json.dumps(tests, default=convert)

    return content #final

def remove_info_prefix(input_string):
    prefix = "INFO-"
    if input_string.startswith(prefix):
        return input_string[len(prefix):]
    else:
        return input_string

def start_monkey_testing(repoInfo, package_name, inputs):
    # Group22-MobileApp-Grupo22-Kotlin - Repo_name for testing
    repo_name = remove_info_prefix(repoInfo)
    build_debug_apk('repos/' + repo_name)

    avd_name = "Pixel_4_API_30"  # Replace "your_avd_name" with the name of your AVD
    start_emulator(avd_name)
    time.sleep(10)
    #apk_path = 'repos/' + directories[0] +"/app/build/outputs/apk/debug/app-debug.apk"
    apk_path = 'repos/' + repo_name +"/app/build/outputs/apk/debug/app-debug.apk"
    
    print(apk_path)
    install_apk(apk_path)
    time.sleep(10)

    path_record = "/sdcard/screenrecord2.mp4"
    start_screen_record(path_record)

    #package_name = "com.example.grupo22_kotlin" # How can we actually get the example name? /as input ig
    #inputs = "2000" # This should also be an input
    output_file = "monkey_test_output.txt"
    run_monkey_test(package_name, inputs, output_file)
    
    stop_screen_record()

    time.sleep(5)
    get_screen_record(path_record)
    
    testsLogInfo = parse_file_to_dict(output_file)
    addTestLog(testsLogInfo, repoInfo)

# if __name__ == "__main__":
    
#     folder_path = 'repos'

#     repos_url = ['https://github.com/Group22-MobileApp/Grupo22-Kotlin.git',
#                  'https://github.com/ISIS3510-202320-Team31/Android-Kotlin.git']
    
#     repos_web = ['https://github.com/camilolcoder/parcial1Web.git']
    
#     #clone_repo_and_update_gitignore(repos_web)

#     directories = list_directories(folder_path)
#     print("Repos to analyse", folder_path, ":", directories)

#     branches = get_branches('repos/' + directories[0])
#     print("Repo  branches", branches)

#     #run_shell_script('repos/' + directories[0])

#     branches = get_branches('repos/' + directories[0])
#     print("Repo  branches", branches)

#     #build_debug_apk('repos/' + directories[0])

#     avd_name = "Pixel_4_API_30"  # Replace "your_avd_name" with the name of your AVD
#     #start_emulator(avd_name)

#     #time.sleep(10)
#     apk_path = 'repos/' + directories[0] +"/app/build/outputs/apk/debug/app-debug.apk"
#     print(apk_path)
#     #install_apk(apk_path)
#     #time.sleep(10)

#     path_record = "/sdcard/screenrecord2.mp4"
#     #start_screen_record(path_record)

#     package_name = "com.example.grupo22_kotlin"
#     inputs = "2000"
#     output_file = "monkey_test_output.txt"
#     #run_monkey_test(package_name, inputs, output_file)
    
#     #stop_screen_record()

#     #time.sleep(5)
#     #get_screen_record(path_record)

#     #npm_install('repos/' + directories[0] + '/parcial1')

#     start_project_front('repos/' + directories[0] + '/parcial1')

