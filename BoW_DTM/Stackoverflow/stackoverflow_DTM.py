import pandas as pd
from BoW_DTM.DTM_class import DTM

stackoverflow_data = pd.read_csv('../../Data/stackoverflow_data.csv')

print(stackoverflow_data.isna().sum())

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


stackoverflow_DTM()