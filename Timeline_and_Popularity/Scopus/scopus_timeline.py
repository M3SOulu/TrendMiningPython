import pandas as pd
from Timeline_and_Popularity.timeline_and_popularity import TimelineAndPopularity   

try:
    scopus_data = pd.read_csv('../../Data/scopus_data.csv', index_col=0)
except FileNotFoundError:
    print("FileNotFoundError: File not found. Please make sure you have mined the data first")
except NameError:
    print("NameError: File not found. Please make sure you have mined the data first")
except Exception as e:
    print("Something went wrong with file reading", e)

scopus_timeline = TimelineAndPopularity(scopus_data)

scopus_timeline.createOutputDir('Scopus')
scopus_timeline.popularityByYears()
scopus_timeline.dailyTrend()
scopus_timeline.citationAnalysis()
scopus_timeline.citationSummary()
scopus_timeline.citationViolinPlot()
scopus_timeline.plotOldvsNewCitations()
scopus_timeline.titleLengthAnalysis()
scopus_timeline.fourWaySplit()
scopus_timeline.getTopArticles()
