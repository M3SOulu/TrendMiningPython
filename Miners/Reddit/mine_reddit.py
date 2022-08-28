import re
import os
import praw  
import pandas as pd
from datetime import datetime   
from dotenv import load_dotenv
from progress.spinner import MoonSpinner, PieSpinner
from Utils.create_file import createFile
from typing import List,  Dict,  Optional

 

load_dotenv() 


reddit_client_id: Optional[str]  =  os.getenv('REDDIT_CLIENT_ID') 
reddit_client_secret: Optional[str] = os.getenv('REDDIT_CLIENT_SECRET') 
reddit_user_agent: Optional[str] = os.getenv('REDDIT_USER_AGENT') 



def cleaner(data: str) -> str:
    """This function is applied to the dataframe, it removes the unnecessary characters  and symbols from it

    Args:
        data (string): Data string that needs to be cleaned

    Returns:
        str: Cleaned string 
    """
    data: str = str(data)  
    res: str = re.sub('\[[^]]*\]' , '', data) #remove eveything in []
    res: str = re.sub("<a.*?>*</a>" , '', data) #remove anchor tags with content
    res: str = re.sub("[0-9]" , '', res) #remove numbers
    res: str = re.sub("&quot", '', res) #remove &quot
    res: str = re.sub("<.*?>", '', res) #remove all HTML tags
    res: str = re.sub("//.*\n", '', res)
    res: str = re.sub("\\{\n.*\\}\n", '', res)
    res: str = re.sub("[\r\n]", '', res)
    res: str = re.sub("\"", '', res) #remove quotes
    res: str = re.sub('[^\w\s]', ' ', res) #remove punctuations
    res: str = res.lower()
    return res

def getData(subreddit: str) -> None:
    """This function mines the data from subreddits

    Args:
        subreddit (str): Name of the subreddit to be mined
    """
    reddit: praw.reddit.Reddit = praw.Reddit(client_id=reddit_client_id,client_secret=reddit_client_secret,user_agent=reddit_user_agent,check_for_async=False)
    subreddit: praw.models.reddit.subreddit.Subreddit = reddit.subreddit(subreddit) 
    print('Subreddit:', subreddit)
    posts= []
    columns=['AuthorId', 'Q_id', 'Title', 'Abstract', 'Answers', 'Cites',  'Date']

    spinner = MoonSpinner('Reddit mining in progress ')
    for post in subreddit.hot(limit=None):
        spinner.next()
        posts.append([post.author, post.id, post.title, 
                  post.selftext, post.num_comments, post.score,
                   datetime.fromtimestamp( post.created) 
                  ])

    spinner.finish()
    reddit_data: pandas.core.frame.DataFrame = pd.DataFrame(posts,columns=columns )

    reddit_data.to_csv('../Data/reddit_data.csv')
    print('Data saved')

def clean_reddit_data() -> None:
    """This function cleans the dataframes by applying the clean_data function to each title and abstract in the dataframe
        Also it drops the row if it has no date and if its abstract is missing
    """
    spinner = PieSpinner('Cleaning Data ') 
    reddit_data = pd.read_csv('../Data/reddit_data.csv', index_col=0)
    reddit_data['Title_clean'] = reddit_data['Title'].apply(cleaner)
    spinner.next()
    abstract = reddit_data.Abstract
    cleaned_abstract = abstract.apply(cleaner)
    reddit_data['Abstract_clean'] = cleaned_abstract
    # Drop the rows which have empty abstract
    reddit_data.drop(reddit_data[reddit_data['Abstract'] == ''].index, inplace=True)
    # Drop rows with no date
    reddit_data.drop(reddit_data[(reddit_data['Date'] == '') | 
                           (reddit_data['Date'] == None) |
                           (reddit_data['Date'] == 0) ].index, 
                           inplace=True
                            )
    # Drop null rows
    reddit_data.dropna(axis=0, inplace=True)
    print("Old file will be replaced\n")
    createFile('reddit_data.csv', '../Data')
    reddit_data.to_csv('../Data/reddit_data.csv')
    spinner.finish()
    print('Data cleaned and saved')

def mine_reddit_data(subreddit) ->  None:
    """High level function used to call all functions needed to mine, clean and save reddit data

    Args:
        subreddit (str): subreddit to be mined
    """
    createFile('reddit_data.csv', '../Data')
    getData(subreddit)
    clean_reddit_data()
    




