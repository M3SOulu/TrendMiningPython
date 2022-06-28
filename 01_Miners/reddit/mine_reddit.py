import re
import os
import praw 
import pandas as pd
from datetime import datetime   
from dotenv import load_dotenv
from progress.spinner import MoonSpinner, PieSpinner



load_dotenv()

REDDIT_CLINT_ID =  os.getenv('REDDIT_CLINT_ID') 
REDDIT_CLINT_SECRET = os.getenv('REDDIT_CLINT_SECRET') 
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT') 

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


def clean_data(data):
    data = str(data)  
    res = re.sub('\[[^]]*\]' , '', data) #remove eveything in []
    res = re.sub("<a.*?>*</a>" , '', data) #remove anchor tags with content
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

def getData(subreddit):
    reddit = praw.Reddit(client_id=REDDIT_CLINT_ID,client_secret=REDDIT_CLINT_SECRET,user_agent=REDDIT_USER_AGENT,check_for_async=False)
    subreddit = reddit.subreddit(subreddit) 
    print('Subreddit:', subreddit)

    posts = []
    columns=['AuthorId', 'Q_id', 'Title', 'Abstract', 'Answers', 'Cites',  'Date']

    spinner = MoonSpinner('Reddit mining in progress ')
    for post in subreddit.hot(limit=None):
        spinner.next()
        posts.append([post.author, post.id, post.title, 
                  post.selftext, post.num_comments, post.score,
                   datetime.fromtimestamp( post.created) 
                  ])

    spinner.finish()
    reddit_data = pd.DataFrame(posts,columns=columns )
    reddit_data.to_csv('../Data/reddit_data.csv')
    print('Data saved')

def clean():
    spinner = PieSpinner('Cleaning Data ') 
    reddit_data = pd.read_csv('../Data/reddit_data.csv')
    reddit_data['Title_clean'] = reddit_data['Title'].apply(clean_data)
    spinner.next()
    abstract = reddit_data.Abstract
    cleaned_abstract = abstract.apply(clean_data)
    reddit_data['Abstract_clean'] = cleaned_abstract
    # Drop the rows which have empty abstract
    reddit_data.drop(reddit_data[reddit_data['Abstract'] == ''].index, inplace=True)
    # Drop rows with no date
    reddit_data.drop(reddit_data[(reddit_data['Date'] == '') | 
                           (reddit_data['Date'] == None) |
                           (reddit_data['Date'] == 0) ].index, 
                           inplace=True
                            )
    createFile('reddit_data.csv')
    reddit_data.to_csv('../Data/reddit_data.csv')
    spinner.finish()
    print('Data cleaned and saved')

def mine_reddit_data(subreddit):
    createFile('reddit_data.csv')
    getData(subreddit)
    clean()
    return




