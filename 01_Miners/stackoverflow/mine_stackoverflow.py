import re
import os
import requests
import pandas as pd
from datetime import datetime   
from dotenv import load_dotenv
from progress.spinner import MoonSpinner, PixelSpinner, PieSpinner


load_dotenv()

API_KEY =  os.getenv('STACKOVERFLOW_API_KEY')
total_filter = 'total'
withbody_filter = 'withbody'

def createFile(file, path = '../Data'):
    doesFolderExist = os.path.exists(path)
    doesFileExist  = os.path.exists(path + '/' + file)
    if (doesFolderExist): 
        # Remove existing stack data file if already exist to add new one
        if (doesFileExist):
            print('Removing already existing',file,'file')
            os.remove(path + '/' + file)
        else:
            print( file + ' does not exist yet, ' + 'it will be downloaded')

    # Create Data folder if did not exist to store the csv file
    else: 
        os.mkdir('../Data')
        print('Data folder created for csv file storage')


def getTotal(stk_query_string):
    total_api_url =  f'https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=activity&q={stk_query_string}&filter={total_filter}&site=stackoverflow&key={API_KEY}'
    res =  requests.get(total_api_url)
    res = res.json()
    total_num = res['total']
    print('total:', total_num)
    return

def fetch_data(query, filter, page_number):
    url = f'https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=activity&q={query}&filter={filter}&site=stackoverflow&key={API_KEY}&page={page_number}'
    res =  requests.get(url)
    res = res.json() 
    return pd.DataFrame(res)


def getBody(stk_query_string):
    spinner = MoonSpinner('Stackoverflow mining in progress ')
    page_number = 1 
    df = fetch_data(stk_query_string, withbody_filter, page_number)

    while df.iloc[-1]['has_more']:
        page_number = page_number + 1
        fetched_data = fetch_data(stk_query_string, withbody_filter, page_number)
        df = pd.concat([df, fetched_data], ignore_index=True) 
        spinner.next()

        if not fetched_data.iloc[-1]['has_more']:
            spinner.finish()
            print(f'Data fetch completed with {len(df)} records')
            break

    # Organize Data
    spinner = PixelSpinner('Organizing data ')
    user_data = []

    for index, row in df.iterrows():
        spinner.next()
        user = {}
        user['AuthorId'] = row['items']['owner'].get('user_id',0)
        user['Q_id'] = row['items'].get('question_id', '') 
        user['Title'] = row['items'].get('title', '')
        user['Abstract'] = row['items'].get('body', '') 
        user['Views'] = row['items'].get('view_count', 0) 
        user['Answers'] = row['items'].get('answer_count', 0)  
        user['Cites'] = row['items'].get('score', 0) 
        user['Tags_n'] = len(row['items'].get('tags', []))  
        user['Tags'] = ';'.join(row['items'].get('tags', ''))
        user['Date'] =  datetime.fromtimestamp( row['items']['creation_date']) 
        user['CR_Date'] =  datetime.fromtimestamp( row['items']['creation_date']) 
        user['LA_Date'] =  datetime.fromtimestamp( row['items']['last_activity_date'])   
        
        user_data.append(user) 
            
    spinner.finish()
    stack_data = pd.DataFrame(data=user_data)
    stack_data.to_csv('../Data/stackoverflow_data.csv')
    print('Data saved')
    return


def clean(data, is_abstract):
    data = str(data)  
    if is_abstract:
        reg_str = "<p>(.*?)</p>" #get only text for abastracts
        res = re.findall(reg_str, data)
        res = ' '.join(res)
    else:
        res = data

    res = re.sub("<a.*?>*</a>" , '', res) #remove anchor tags with content
    res = re.sub("[0-9]" , '', res) #remove numbers
    res = re.sub("&quot", '', res) #remove &quot
    res = re.sub("<.*?>", '', res) #remove all HTML tags
    res = re.sub("//.*\n", '', res)
    res = re.sub("\\{\n.*\\}\n", '', res)
    res = re.sub("[\r\n]", '', res)
    res = re.sub("\"", '', res) #remove quotes
    res = re.sub('[^\w\s]', ' ', res) #remove punctuations
    res = res.lower()

    return res

def cleanData():
    spinner = PieSpinner('Cleaning Data ')
    stack_data = pd.read_csv('../Data/stackoverflow_data.csv')
    abstract = stack_data.Abstract
    cleaned_abstract = abstract.apply(clean, is_abstract=True)
    stack_data['Abstract_clean'] = cleaned_abstract

    #Drop rows where abstract has empty value
    stack_data.drop(stack_data[stack_data['Abstract'] == ''].index, inplace=True)

    #Drop rows with no date
    stack_data.drop(stack_data[(stack_data['Date'] == '') | (stack_data['Date'] == None) | (stack_data['Date'] == 0) ].index, inplace=True)
    createFile('stackoverflow_data.csv')
    stack_data.to_csv('../Data/stackoverflow_data.csv')
    spinner.finish()
    print('Data cleaned and saved')
    return

def mine_stackoverflow_data(searchKeyword):
    createFile('stackoverflow_data.csv')
    getTotal(searchKeyword)
    getBody(searchKeyword)
    cleanData()
    return


 




