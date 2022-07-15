import pandas as pd
from BoW_DTM.DTM_class import DTM


try:
    reddit_data = pd.read_csv('../../Data/reddit_data.csv')
except FileNotFoundError:
    print("FileNotFoundError: File not found. Please make sure you have mined the data first")
except NameError:
    print("NameError: File not found. Please make sure you have mined the data first")
except Exception as e:
    print("Something went wrong with file reading", e)

def reddit_DTM():
    reddit_data_DTM = DTM(reddit_data)
    reddit_data_DTM.createOutputDir("Reddit")
    reddit_data_DTM.remove_stop_words(["new", "custom", "words", "add","to","list", "d"])
    reddit_data_DTM.combine_title_and_abs()
    reddit_data_DTM.stemming()
    reddit_data_DTM.document_term_matrix('Tokenized_data') # pass the column for whcih you want to generate DTM 
    reddit_data_DTM.frequent_terms()  
    reddit_data_DTM.print_frequent_words(3)
    reddit_data_DTM.sort_frequent_terms()  
    reddit_data_DTM.print_sorted_frequent_words(3)
    reddit_data_DTM.keep_top_words()  
    reddit_data_DTM.print_top_words(3)
    reddit_data_DTM.visualize_frequent_words()
    reddit_data_DTM.dendogram_clusting()
    reddit_data_DTM.saveFile('reddit_data.csv', '../../Data')

reddit_DTM()