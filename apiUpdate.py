from dotenv import load_dotenv
from github import Github , InputGitTreeElement
import pygsheets
import yaml
import datetime
import os

update_file_name = ['日語.yaml', '國語.yaml', '粵語.yaml', '英語.yaml', '韓語.yaml', 
                    '意義不明.yaml', '演唱會-音樂節目-BGM.yaml', '台語-其他.yaml']

def getTreeElement(file_path, repo):
    # get the file content from local
    with open(f'playlist/{file_path}', 'r', encoding='utf-8') as f:
        content = f.read()

    # get the file content from github
    gitContent = repo.get_contents(file_path)
    decodeGitContent = gitContent.decoded_content.decode('utf-8')

    # check if the file need to update
    if content == decodeGitContent:
        return None

    # create a new blob
    blob = repo.create_git_blob(content, 'utf-8')
    # create a new tree element
    element = InputGitTreeElement(path=file_path, mode='100644', type='blob', sha=blob.sha)
    return element

def getRepoAndElements():
    access_token = os.getenv('GITHUB_ACCESS_TOKEN')
    repo_name = os.getenv('GITHUB_REPO_NAME')

    # login github and get the repo
    g = Github(access_token)
    repo = g.get_repo(repo_name)
    
    element_arr = []
    for file_name in update_file_name:
        e = getTreeElement(file_name, repo)
        if e != None:
            element_arr.append(e)
    
    return element_arr, repo

def updateFiles(element_arr, repo):
     # get the head(main) commit infomation
    ref = repo.get_git_ref('heads/main')
    head_sha = ref.object.sha

    # create a new tree
    base_tree = repo.get_git_tree(sha=head_sha)
    tree = repo.create_git_tree(element_arr, base_tree)
    parent = repo.get_git_commit(sha=head_sha)

    # create a new commit
    curr_date = datetime.datetime.now().strftime('%Y-%m-%d')
    commit_msg = f'Daily Update - {curr_date}'
    commit = repo.create_git_commit(commit_msg, tree, [parent])

    # update the head
    ref.edit(commit.sha)

def getSheetData():
    token_file_name = os.getenv('GOOGLE_SHEET_TOKEN_FILE')
    sheet_url = os.getenv('GOOGLE_SHEET_URL')
    # authorization
    gc = pygsheets.authorize(service_file=token_file_name)
    # Open spreadsheet and then worksheet
    sh = gc.open_by_url(sheet_url)
    return sh

def saveSheetData(sh):
    wks_list = sh.worksheets()
    for wks in wks_list:
        yamlData = []
        wks_title = wks.title
        if wks_title == '心情':
            continue
        data = wks.get_as_df()
        for index, row in data.iterrows():
            # print(row[0], row[1], row[2], row[3])
            theRow = {
                'artist': str(row[0]).strip(),
                'music': str(row[1]).strip(),
                'allName': row[2].strip(),
                'url': row[3].strip()
            }
            yamlData.append(theRow)

        with open(f'playlist/{wks_title}.yaml', 'w', encoding='utf-8') as file:
            yaml.dump(yamlData, file, allow_unicode=True)
   
if __name__ == '__main__':
    load_dotenv()
    print('[*] Start get sheet data')
    sh = getSheetData()
    print('[*] Get sheet data success')
    print('-' * 50)

    print('[*] Start save sheet data')
    saveSheetData(sh)
    print('[*] Save sheet data success')
    print('-' * 50)

    print('[*] Start get new elements')
    element_arr, repo = getRepoAndElements() 
    if len(element_arr) == 0:
        print('[-] No files need to update')
        os._exit(0)
    print('[*] Get new elements success')
    print('-' * 50)

    print('[*] Start update files to github')
    updateFiles(element_arr, repo)
    print('[*] Update files success')
