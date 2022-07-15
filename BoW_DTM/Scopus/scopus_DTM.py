import pandas as pd
from BoW_DTM.DTM_class import DTM


try:
    scopus_data = pd.read_csv('../../Data/scopus_data.csv')
except FileNotFoundError:
    print("FileNotFoundError: File not found. Please make sure you have mined the data first")
except NameError:
    print("NameError: File not found. Please make sure you have mined the data first")
except Exception as e:
    print("Something went wrong with file reading", e)

def scopus_DTM():
    scopus_data_DTM = DTM(scopus_data)
    scopus_data_DTM.createOutputDir("Scopus")
    scopus_data_DTM.remove_stop_words(["new", "custom", "words", "add","to","list", "d"])
    scopus_data_DTM.combine_title_and_abs()
    scopus_data_DTM.stemming()
    scopus_data_DTM.document_term_matrix('Tokenized_data') # pass the column for whcih you want to generate DTM 
    scopus_data_DTM.frequent_terms()  
    scopus_data_DTM.print_frequent_words(3)
    scopus_data_DTM.sort_frequent_terms()  
    scopus_data_DTM.print_sorted_frequent_words(3)
    scopus_data_DTM.keep_top_words()  
    scopus_data_DTM.print_top_words(3)
    scopus_data_DTM.visualize_frequent_words()
    scopus_data_DTM.dendogram_clusting()
    scopus_data_DTM.saveFile('scopus_data.csv', '../../Data')


scopus_DTM()