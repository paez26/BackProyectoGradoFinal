import pandas as pd
from pydriller import Repository
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
from gitclone import main
import json
import numpy as np
import json
from bson import json_util
from joblib import load


def pydriller(url:str, nameinfo:str):
        path = main(url)
        #path= 'repos\caev03-ISIS3710_202320_S2_E08_back.git'

        df = pd.DataFrame()
        repo = Repository(path  , only_in_branch="Dev")
        repo_commits = repo.traverse_commits()
        for commit in repo_commits:
                df = pd.concat([df, pd.DataFrame({
                                                "msg" : [commit.msg],
                                                        'author_name': [commit.author.name],
                                                        'commiter_email': [commit.committer.email],
                                                        'num_inserts': [commit.insertions],
                                                        "num_deletes": [commit.deletions],
                                                        "net_lines": [commit.insertions - commit.deletions],
                                                        "author_Date": [commit.author_date]
                                                        })])
        df = df[~df['commiter_email'].str.contains('noreply@github.com')]
        df['commiter_email'] = df['commiter_email'].str.split('@').str[0]
        df['commiter_email'] = df['commiter_email'].str.split('+').str[-1]
        df = df.drop(columns=['author_name'])
        df = df.rename(columns={'commiter_email': 'author_name'})
        df = df[~df['msg'].str.contains("Merge branch 'Dev'")]
        df = df[~df['msg'].str.contains("merge")]
        df = df[~df['msg'].str.contains("Merge")]
        df = df[~df['msg'].str.contains('Lisan Algaib')] # This commit is the creation of the project
        contributions = dict(df.groupby('author_name').sum().sort_values(by='net_lines', ascending=False))
        authors =df['author_name'].unique()
        superdic={}
        for x in authors:
                dic={}
                for y in contributions:
                        dic[y]= contributions[y][x]
                superdic[x]=dic
        tt = pd.DataFrame()

        repo = Repository(path , only_in_branch="Dev")
        repo_commits = repo.traverse_commits()

        for commit in repo_commits:
                for f in commit.modified_files:
                        tt = pd.concat([tt, pd.DataFrame({
                                                        'author_name': [commit.author.name],
                                                        'commiter_email': [commit.author.email],
                                                        "file": [f.filename],
                                                        "msg" : [commit.msg]
                                                        })])
        tt = tt[~tt['commiter_email'].str.contains('noreply@github.com')]
        tt['commiter_email'] = tt['commiter_email'].str.split('@').str[0]
        tt['commiter_email'] = tt['commiter_email'].str.split('+').str[-1]
        tt = tt.drop(columns=['author_name'])
        tt = tt.rename(columns={'commiter_email': 'author_name'})
        tt = tt[~tt['msg'].str.contains('Lisan Algaib')]
        authors = tt['author_name'].value_counts()
        for x in authors.index:
                gg=dict(tt[tt['author_name'] == x]['file'].value_counts().head(5))
                filesDict={}
                for y in gg:
                        filesDict[y]=gg[y]

                superdic[x]['files']=filesDict
        da= dict(tt["author_name"].value_counts())
        for x in da:
                superdic[x]['commits']=da[x]
                #promedio de lineas por commit
                superdic[x]['avg_lines']=superdic[x]['net_lines']/da[x]
        for x in superdic:
                t=(df[df['author_name'] == x])
                #get only the num insert and date
                t=t[['num_inserts','author_Date']]
                #pass the date to datetime
                t['author_Date'] = pd.to_datetime(t['author_Date'], errors='coerce', utc=True)
                # only show the month
                t['author_Date'] = t['author_Date'].dt.to_period('M')
                #group by month and sum the num insertions
                t=t.groupby('author_Date').sum()
                pelo = t.to_dict()
                # pass t to a dataframe
                fechas = {}
                for z in pelo['num_inserts']:
                        fechas[str(z)] = pelo['num_inserts'][z]

                # put the data in superdic
                superdic[x]['inserts']=fechas

        df = pd.DataFrame()

        repo = Repository(path, only_in_branch="Dev")
        repo_commits = repo.traverse_commits()
        for commit in repo_commits:
                df = pd.concat([df, pd.DataFrame({
                                                "msg" : [commit.msg],
                                                        'author_name': [commit.author.name],
                                                        'commiter_email': [commit.committer.email],
                                                        'dmm_unit_size ': [commit.dmm_unit_size],
                                                        'dmm_unit_complexity ': [commit.dmm_unit_complexity],
                                                        'dmm_unit_interfacing ': [commit.dmm_unit_interfacing]
                                                        })])
        df = df[~df['commiter_email'].str.contains('noreply@github.com')]
        # delete the rows that columns msg has merge in it
        df = df[~df['msg'].str.contains("merge")]
        df = df[~df['msg'].str.contains("Merge")]
        df['commiter_email'] = df['commiter_email'].str.split('@').str[0]
        df['commiter_email'] = df['commiter_email'].str.split('+').str[-1]
        df = df.drop(columns=['author_name'])
        df = df.rename(columns={'commiter_email': 'author_name'})
        df = df[~df['msg'].str.contains('Lisan Algaib')]
        # Clean column names
        df.columns = df.columns.str.strip()

        # Filter the DataFrame by author_name
        dictRepositorio={}



        promedio_dmm_unit_size = df['dmm_unit_size'].mean()


        promedio_dmm_unit_complexity = df['dmm_unit_complexity'].mean()


        promedio_dmm_unit_interfacing = df['dmm_unit_interfacing'].mean()

        model = load('pipe.joblib')
        df['goodPractices'] = model.predict(df["msg"])
        good_practices_group = df['goodPractices'].sum() / len(df) * 100
        contributions_by_author = (df.groupby('author_name').mean()* 100)

        dictRepositorio["promedio_dmm_unit_size"] = promedio_dmm_unit_size
        dictRepositorio["promedio_dmm_unit_complexity"] = promedio_dmm_unit_complexity
        dictRepositorio["promedio_dmm_unit_interfacing"] = promedio_dmm_unit_interfacing
        dictRepositorio["good_practices_group"] = good_practices_group
        dictRepositorio["owner_repo"] = nameinfo

        contributions_by_author  = contributions_by_author.to_dict()

        authors =df['author_name'].unique()
        metrics = ['dmm_unit_size', 'dmm_unit_complexity', 'dmm_unit_interfacing', 'goodPractices']
        for x in authors:
                for y in metrics:


                        superdic[x][y] = 0

        for metric, users in contributions_by_author.items():
                for user, value in users.items():
                        if not np.isnan(value):  # Check if the value is not NaN
                                superdic[user][metric] = value
                        else:
                                superdic[user][metric] = 0







        print(superdic)
        print(dictRepositorio)
        dictRepositorio["id_repo"] = nameinfo

        superdic["owner"] = nameinfo


        def convert(obj):
                if isinstance(obj, np.int64):
                        return int(obj)
                return obj

        # Convert dictionary to JSON
        final = json.dumps(superdic, default=convert)

        return final , dictRepositorio




#pydriller("https://github.com/Group22-MobileApp/Grupo22-Kotlin/","d")