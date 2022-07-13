import re
import os
import pandas as pd
import pybliometrics 
from datetime import datetime   
from dotenv import load_dotenv
from Utils.create_file import createFile
from pybliometrics.scopus import ScopusSearch
from pybliometrics.scopus.utils import config 

from progress.spinner import MoonSpinner, PieSpinner


load_dotenv()

scopus_api_key =  os.getenv('SCOPUS_API_KEY')
 
 
def clean_scopus_data(data):
    """This function is applied to the dataframe, it removes the unnecessary characters  and symbols from it

    Args:
        data (string): Data string that needs to be cleaned

    Returns:
        str: Cleaned string 
    """
    data = str(data)
    res = re.sub("[©®™%]", "", data) #remove ©,®,™,% sign 
    res = re.sub("<a.*?>*</a>", '', data) #remove anchor tags with content
    res = re.sub("[0-9]", '', res) #remove numbers
    res = re.sub("<.*?>", '', res) #remove all HTML tags
    res = re.sub("//.*\n", '', res)
    res = re.sub("\\{\n.*\\}\n", '', res)
    res = re.sub("[\r\n]", '', res)
    res = re.sub("\"", '', res) #remove quotes
    res = re.sub('[^\w\s]', ' ', res) #remove punctuations
    res = re.sub("All right reserved[.]", ' ', res) #
    res = data.lower()
    return res


def getData(query):
    """This function mines the Scopus database

    Args:
        query (str): query or string that will be used as a criteria while mining
    """
    spinner = MoonSpinner('Scopus mining in progress ')
    scopus_query = query
    scopus_res = ScopusSearch(scopus_query,  download=True, view='COMPLETE')
    print('Total entries', scopus_res.get_results_size()) 

    scopus_data = pd.DataFrame(pd.DataFrame(scopus_res.results))
    print('Dataframe shape', scopus_data.shape)

    spinner.next()
    scopus_data_subset = scopus_data[['eid', 'doi', 'title', 'creator', 'publicationName', 'coverDate', 'description', 
                           'authkeywords', 'citedby_count', 'pageRange', 'aggregationType', 'subtypeDescription',
                          'author_count', 'author_names', 'author_ids', 'affilname', 'affiliation_country'
                          ]]
    spinner.finish() 
    scopus_data_subset.to_csv('../Data/scopus_data.csv')
    print('Data saved')
     
 

def clean():
    """
    This function cleans the dataframes by applying the clean_scopus_data function to each abstract in the dataframe
        Also it renames few important column names  
    """
    spinner = PieSpinner('Cleaning Data ')
    scopus_data_subset = pd.read_csv('../Data/scopus_data.csv')
    abstract = scopus_data_subset['description']
    cleaned_abstract = abstract.apply(clean_scopus_data)
    scopus_data_subset['Abstract_clean'] = cleaned_abstract 
    scopus_data_subset.rename(columns={'description':'Abstract', 'coverDate': 'Date', 'citedby_count': 'Cites', 'title': 'Title'}, inplace=True)
    scopus_data_subset.to_csv('../Data/scopus_data.csv')
    spinner.finish()
    print('Data cleaned and saved')
     
    # TODO: Remove papers that are summaries of conference proceedings. 
     


def mine_scopus_data(query):
    """High level function used to call all functions needed to mine, clean and save scopus data

    Args:
        query (str): query or string that will be used as a criteria while mining
    """
    createFile('scopus_data.csv', '../Data')
    print("Enter this key when prompted to enter key:", scopus_api_key)
    pybliometrics.scopus.utils.create_config()
    print('API key set', config['Authentication']['APIKey'])  
    getData(query)
    clean()



