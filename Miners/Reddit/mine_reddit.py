import re
import os
import praw  
import pandas as pd
from datetime import datetime   
from dotenv import load_dotenv
from progress.spinner import MoonSpinner, PieSpinner

 

load_dotenv() 


reddit_client_id =  os.getenv('REDDIT_CLIENT_ID') 
reddit_client_secret = os.getenv('REDDIT_CLIENT_SECRET') 
reddit_user_agent = os.getenv('REDDIT_USER_AGENT') 

def createFile(file, path):
    """This function is used to create the directory necessary to store the mined data.        

    Args:
        file (str): Name of the file to be created.
        path (str): Path of the directory where the files will be stored e.g. "../../Data".
    """
    does_folder_exist = os.path.exists(path)
    does_file_exist  = os.path.exists(path + '/' + file)
    if (does_folder_exist): 
        # Remove existing stack data file if already exist to add new one
        if (does_file_exist):
            print('Removing already existing',file,'file')
            os.remove(path + '/' + file)
        else:
            print( file + ' does not exist yet, ' + 'it will be downloaded')

    # Create Data folder if did not exist to store the csv file
    else: 
        os.mkdir('../Data')
        print('Data folder created for csv file storage')

def clean_data(data):
    """This function is applied to the dataframe, it removes the unnecessary characters  and symbols from it

    Args:
        data (string): Data string that needs to be cleaned

    Returns:
        str: Cleaned string 
    """
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
    """This function mines the data from subreddits

    Args:
        subreddit (str): Name of the subreddit to be mined
    """
    reddit = praw.Reddit(client_id=reddit_client_id,client_secret=reddit_client_secret,user_agent=reddit_user_agent,check_for_async=False)
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

def clean_reddit_data():
    """This function cleans the dataframes by applying the clean_data function to each title and abstract in the dataframe
        Also it drops the row if it has no date and if its abstract is missing
    """
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
    createFile('reddit_data.csv', '../Data')
    reddit_data.to_csv('../Data/reddit_data.csv')
    spinner.finish()
    print('Data cleaned and saved')

def mine_reddit_data(subreddit):
    """High level function used to call all functions needed to mine, clean and save reddit data

    Args:
        subreddit (str): subreddit to be mined
    """
    createFile('reddit_data.csv', '../Data')
    getData(subreddit)
    clean_reddit_data()
    




