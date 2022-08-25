import pandas as pd
from Timeline_and_Popularity.timeline_and_popularity import TimelineAndPopularity   

try:
    stackoverflow_data = pd.read_csv('../../Data/stackoverflow_data.csv', index_col=0)
except FileNotFoundError:
    print("FileNotFoundError: File not found. Please make sure you have mined the data first")
except NameError:
    print("NameError: File not found. Please make sure you have mined the data first")
except Exception as e:
    print("Something went wrong with file reading", e)

stackoverflow_timeline = TimelineAndPopularity(stackoverflow_data)

stackoverflow_timeline.createOutputDir('Stackoverflow')
stackoverflow_timeline.popularityByYears()
stackoverflow_timeline.dailyTrend()
stackoverflow_timeline.citationAnalysis()
stackoverflow_timeline.citationSummary()
stackoverflow_timeline.citationViolinPlot()
stackoverflow_timeline.plotOldvsNewCitations()
stackoverflow_timeline.titleLengthAnalysis()
stackoverflow_timeline.fourWaySplit()
stackoverflow_timeline.getTopArticles()
