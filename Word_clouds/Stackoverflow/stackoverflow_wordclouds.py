import pandas as pd
from Word_clouds.cloud_generator import WordCloudGenerator

try:
    stackoverflow_data = pd.read_csv('../../Data/stackoverflow_data.csv', index_col=0)
except FileNotFoundError:
    print("FileNotFoundError: File not found. Please make sure you have mined the data first")
except NameError:
    print("NameError: File not found. Please make sure you have mined the data first")
except Exception as e:
    print("Something went wrong with file reading", e)


stackoverflow_data = WordCloudGenerator(stackoverflow_data)

stackoverflow_data.createOutputDir('Stackoverflow')

stackoverflow_data.make_word_clouds('Abstrat_without_stopwords', max_words=55, scale=3)

stackoverflow_data.date_based_comparasion_cloud()