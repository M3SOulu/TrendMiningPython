import os
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon
import seaborn as sns

class TimelineAndPopularity():
    """This is the class implementation for timeline and popularity
    """
    def __init__(self, data_frame):
        self.data_frame = data_frame 
        self.dirName = ""

    def createOutputDir(self, dirName):
        """This function creates output directory for file storage

        Args:
            dirName (str): Name of the directory you want to create
        """
        self.dirName = dirName
        does_folder_exist = os.path.exists(f'../Output/{dirName}')
        if (does_folder_exist):
            print("Output directory already exists.")         
        else:
            os.makedirs(f'../Output/{dirName}')
        print('Folder created for output storage')  

    def popularityByYears(self):
        """This function calculated the popularity over the years
        """
        self.data_frame['Date'] = self.data_frame['Date'].apply(lambda x: pd.to_datetime(str(x), format='%Y-%m-%d', yearfirst=True)).dt.date
        years = pd.DatetimeIndex(self.data_frame['Date']).year
        year_count =  Counter(years)
        print('Yearly distributions:', year_count)
        sns.lineplot(data=year_count).set(title=f"{self.dirName} yearly popularity")
        plt.xticks(rotation=90)
        plt.show()
        plt.savefig(os.path.join("../Output/" + self.dirName, f"{self.dirName}_yearly_popularity.png"))
        print('Yearly popularity figure saved')

    def dailyTrend(self):
        """This function calculates the daily trend
        """
        days =  pd.to_datetime(self.data_frame['Date']).dt.date 
        days_count =  Counter(days) 
        sns.lineplot(data=days_count).set(title=f"{self.dirName} daily trend")
        plt.xticks(rotation=90)
        plt.show()
        plt.savefig(os.path.join("../Output/" + self.dirName, f"{self.dirName}_daily_trend.png"))
        print('Daily trend Figure saved')

    def citationAnalysis(self):
        """This function calculates boxplot for the citations 
        """
        citations = self.data_frame['Cites']
        sns.boxplot(citations, orient='h').set(title=f"{self.dirName} citation boxPlot")
        plt.show()
        plt.savefig(os.path.join("../Output/" + self.dirName, f"{self.dirName}_citation_boxPlot.png"))
        print('Citation boxplot figure saved')
    
    def citationSummary(self):
        """This function calculates statistical summary for citations
        """
        citations = self.data_frame['Cites']
        print('Citation Summary:')
        print(citations.describe())

    def citationViolinPlot(self):
        """This function calculates the violin plot for citations
        """
        citations = self.data_frame['Cites']
        sns.violinplot(x=citations).set(title=f"{self.dirName} citation violinPlot")
        plt.show()
        plt.savefig(os.path.join("../Output/" + self.dirName, f"{self.dirName}_citation_violinPlot.png"))
        print('Citation violinplot figure saved')
    
    def plotOldvsNewCitations(self):
        """This function calculated old and new citations based on median of date
        """
        mid_date = self.data_frame['Date'].astype('datetime64[ns]').quantile(0.5, interpolation="midpoint")
        new_data = self.data_frame[self.data_frame['Date']>= mid_date]
        old_data = self.data_frame[self.data_frame['Date'] < mid_date]
        print('Median date is:',mid_date)    
       
        # Box plots
        fig, axes = plt.subplots(1, 2)
        sns.boxplot(old_data['Cites'],  ax=axes[0])
        axes[0].set_title("Old Data")
        sns.boxplot(new_data['Cites'],  ax=axes[1])
        axes[1].set_title("New Data")
        # plt.show()
        plt.savefig(os.path.join("../Output/" + self.dirName, f"{self.dirName}_oldVSnew_boxPlot.png"))
        print('Old vs new boxplot figure saved')

        # Voilen plots
        fig, axes = plt.subplots(1, 2)
        sns.violinplot(old_data['Cites'],  ax=axes[0])
        axes[0].set_title("Old Data")
        sns.violinplot(new_data['Cites'],  ax=axes[1])
        axes[1].set_title("New Data")
        plt.show()
        plt.savefig(os.path.join("../Output/" + self.dirName, f"{self.dirName}_oldVSnew_violinPlot.png"))
        print('Old vs new violinplot figure saved')


        # Summary of old and new
        print("Old Data Summary")
        print(old_data['Cites'].describe())
        print("New Data Summary")
        print(new_data['Cites'].describe())

    def titleLengthAnalysis(self):
        """This function calculates old and new titles based on median of the length of title
        """
        title_lens = self.data_frame['Title'].str.len()
        median_len = title_lens.median()
        longer_length_data = self.data_frame[self.data_frame['Title'].str.len() >= median_len]
        shorter_length_data = self.data_frame[self.data_frame['Title'].str.len() < median_len]
        print('Total data points', len(self.data_frame))
        print('Total data points with longer title', len(longer_length_data))
        print('Total data points with shorter title', len(shorter_length_data))

        # Box plots
        fig, axes = plt.subplots(1, 2)
        sns.boxplot(longer_length_data['Cites'],  ax=axes[0])
        axes[0].set_title("Longer Data")
        sns.boxplot(shorter_length_data['Cites'],  ax=axes[1])
        axes[1].set_title("Shorter Data")
        # plt.show()
        plt.savefig(os.path.join("../Output/" + self.dirName, f"{self.dirName}_titleLength_boxPlot.png"))
        print('Title length boxplot figure saved')
        

        # Voilen plots
        fig, axes = plt.subplots(1, 2)
        sns.violinplot(longer_length_data['Cites'],  ax=axes[0])
        axes[0].set_title("Longer Data")
        sns.violinplot(shorter_length_data['Cites'],  ax=axes[1])
        axes[1].set_title("Shorter Data")
        plt.show()
        plt.savefig(os.path.join("../Output/" + self.dirName, f"{self.dirName}_titleLength_violinPlot.png"))
        print('Title length violinplot figure saved')

        # Summary of old and new
        print("Longer Data Summary")
        print(longer_length_data['Cites'].describe())
        print("Shorter Data Summary")
        print(shorter_length_data['Cites'].describe())

        # Wilcoxon
        w, p = wilcoxon(longer_length_data['Cites'])
        print('Wilcoxon for longer')
        print('W:', w, 'P:', p)
        w, p = wilcoxon(shorter_length_data['Cites'])
        print('Wilcoxon for shorter')
        print('W:', w, 'P:', p)

    def fourWaySplit(self):
        """This function splits the title in four parts based on the four quantiles.
        """
        title_lens = self.data_frame['Title'].str.len()
        q1 = self.data_frame[self.data_frame['Title'].str.len() == title_lens.quantile(0.25, interpolation='midpoint')]
        q2 = self.data_frame[self.data_frame['Title'].str.len() > title_lens.quantile(0.25, interpolation='midpoint')]
        q3 = self.data_frame[self.data_frame['Title'].str.len() <= title_lens.quantile(0.50,  interpolation='midpoint')]
        q4 = self.data_frame[self.data_frame['Title'].str.len() > title_lens.quantile(0.75,  interpolation='midpoint')]
        print('Total length of data:', len(self.data_frame))
        print('Length of q1:', len(q1))
        print('Length of q2:', len(q2))
        print('Length of q3:', len(q3))
        print('Length of q4:', len(q4))
        
        # Box plots
        fig, axes = plt.subplots(1, 4)
        sns.boxplot(q1['Cites'],  ax=axes[0])
        axes[0].set_title("Q1 Data")
        sns.boxplot(q2['Cites'],  ax=axes[1])
        axes[1].set_title("Q2 Data")
        sns.boxplot(q3['Cites'],  ax=axes[2])
        axes[2].set_title("Q3 Data")
        sns.boxplot(q4['Cites'],  ax=axes[3])
        axes[3].set_title("Q4 Data")
        plt.show()
        plt.savefig(os.path.join("../Output/" + self.dirName, f"{self.dirName}_FourwaySplit_boxPlot.png"))
        print('Four way figure saved')
        
        #Summary of data
        print('Q1 Cites Summary:')
        print(q1['Cites'].describe())
        print('Q2 Cites Summary:')
        print(q2['Cites'].describe())
        print('Q3 Cites Summary:')
        print(q3['Cites'].describe())
        print('Q4 Cites Summary:')
        print(q4['Cites'].describe())

    def getTopArticles(self):
        """This function calculates top article based on the citation
        """
        sorted_df = self.data_frame.sort_values(by=['Cites'],ascending=False) 
        combined = pd.DataFrame({'Title':sorted_df['Title_clean'], 'cites':sorted_df['Cites']})
        print('Top 5 articles')
        print(combined.head(5))
    




