import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud

class WordCloudGenerator():
    def __init__(self, data_frame):
        self.data_frame = data_frame 
        self.dirName = ""

    def createOutputDir(self, dirName):
        self.dirName = dirName
        does_folder_exist = os.path.exists(f'../Output/{dirName}')
        if (does_folder_exist):
            print("Output directory already exists.")         
        else:
            os.makedirs(f'../Output/{dirName}')
        print('Folder created for output storage')  

    def make_word_clouds(self, column, max_words=50, scale=2):
        strings  = ' '.join(self.data_frame[column])
        wordcloud = WordCloud(scale=2, max_words=50, background_color="white").generate(strings)
        plt.figure(figsize = (20, 20))
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.show()
        plt.savefig(os.path.join("../Output/" + self.dirName, f"{self.dirName}_word_cloud.png"))


    def date_based_comparasion_cloud(self):
        mid_date = self.data_frame['Date'].astype('datetime64[ns]').quantile(0.5, interpolation="midpoint")
        new_titles = self.data_frame[(self.data_frame['Date']).astype('datetime64[ns]') >= mid_date]
        old_titles = self.data_frame[(self.data_frame['Date']).astype('datetime64[ns]') <  mid_date] 
        titles = [old_titles, new_titles] 
        print(mid_date)
        for i in range(len(titles)):  
            try:
                strings = ' '.join(titles[i]['Title_without_stopwords'])
                wordcloud = WordCloud(scale=2, max_words=50, background_color="white").generate(strings) 
                plt.subplot(2, 2, i+1)
                plt.imshow(wordcloud, interpolation="bilinear")
                plt.axis("off")
                if i == 0:
                    plt.title(f'Old Titles before or during {mid_date.date()}')
                else:
                    plt.title(f'New Titles after {mid_date.date()}')
            except:
                continue
            
        plt.show()
        plt.savefig(os.path.join("../Output/" + self.dirName, f"{self.dirName}_comparison_cloud.png"))
             
            
                