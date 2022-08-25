import pandas as pd
from Word_clouds.cloud_generator import WordCloudGenerator

try:
    reddit_data = pd.read_csv('../../Data/reddit_data.csv', index_col=0)
except FileNotFoundError:
    print("FileNotFoundError: File not found. Please make sure you have mined the data first")
except NameError:
    print("NameError: File not found. Please make sure you have mined the data first")
except Exception as e:
    print("Something went wrong with file reading", e)


reddit_cloud = WordCloudGenerator(reddit_data)

reddit_cloud.createOutputDir('Reddit')

reddit_cloud.make_word_clouds('Abstrat_without_stopwords', max_words=55, scale=3)

reddit_cloud.date_based_comparasion_cloud()