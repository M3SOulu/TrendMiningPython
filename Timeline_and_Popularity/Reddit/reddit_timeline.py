import pandas as pd
from Timeline_and_Popularity.timeline_and_popularity import TimelineAndPopularity   

try:
    reddit_data = pd.read_csv('../../Data/reddit_data.csv', index_col=0)
except FileNotFoundError:
    print("FileNotFoundError: File not found. Please make sure you have mined the data first")
except NameError:
    print("NameError: File not found. Please make sure you have mined the data first")
except Exception as e:
    print("Something went wrong with file reading", e)

reddit_timeline = TimelineAndPopularity(reddit_data)

reddit_timeline.createOutputDir('Reddit')
reddit_timeline.popularityByYears()
reddit_timeline.dailyTrend()
reddit_timeline.citationAnalysis()
reddit_timeline.citationSummary()
reddit_timeline.citationViolinPlot()
reddit_timeline.plotOldvsNewCitations()
reddit_timeline.titleLengthAnalysis()
reddit_timeline.fourWaySplit()
reddit_timeline.getTopArticles()
