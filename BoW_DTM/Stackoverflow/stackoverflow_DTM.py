import pandas as pd
from BoW_DTM.DTM_class import DTM

try:
    stackoverflow_data = pd.read_csv('../../Data/stackoverflow_data.csv', index_col=0)
except FileNotFoundError:
    print("FileNotFoundError: File not found. Please make sure you have mined the data first")
except NameError:
    print( "NameError: File not found. Please make sure you have mined the data first")
except Exception as e:
    print("Something went wrong with file reading", e)

def stackoverflow_DTM():
    stackoverflow_data_DTM = DTM(stackoverflow_data)
    stackoverflow_data_DTM.createOutputDir("Stackoverflow")
    stackoverflow_data_DTM.remove_stop_words(["new", "custom", "words", "add","to","list", "d"])
    stackoverflow_data_DTM.combine_title_and_abs()
    stackoverflow_data_DTM.stemming()
    stackoverflow_data_DTM.document_term_matrix('Tokenized_data') # pass the column for whcih you want to generate DTM 
    stackoverflow_data_DTM.frequent_terms()  
    stackoverflow_data_DTM.print_frequent_words(3)
    stackoverflow_data_DTM.sort_frequent_terms()  
    stackoverflow_data_DTM.print_sorted_frequent_words(3)
    stackoverflow_data_DTM.keep_top_words()  
    stackoverflow_data_DTM.print_top_words(3)
    stackoverflow_data_DTM.visualize_frequent_words()
    stackoverflow_data_DTM.dendogram_clusting()
    stackoverflow_data_DTM.saveFile('stackoverflow_data.csv', '../../Data')


stackoverflow_DTM()