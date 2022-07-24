import pandas as pd
from Word_clouds.cloud_generator import WordCloudGenerator

try:
    scopus_data = pd.read_csv('../../Data/scopus_data.csv')
except FileNotFoundError:
    print("FileNotFoundError: File not found. Please make sure you have mined the data first")
except NameError:
    print("NameError: File not found. Please make sure you have mined the data first")
except Exception as e:
    print("Something went wrong with file reading", e)


scopus_data = WordCloudGenerator(scopus_data)

scopus_data.createOutputDir('Scopus')

scopus_data.make_word_clouds('Abstrat_without_stopwords', max_words=55, scale=3)

scopus_data.date_based_comparasion_cloud()