# TrendMining

Trend Mining project

## Setup Anaconda

- Start by [setting up anaconda](https://www.anaconda.com/products/distribution).
- Open the Anaconda Navigator.
- Once inside click on `Environments`.
- Click on the `Create`.
- Name the environment `trendMiningEnv` or whatever you want, also select packages as `python` with version `3.8` 
- Once the new environment is created navigate back to `Home` screen in Anaconda Navigator.
- Make sure you have `VS Code` and `CMD.exe Prompt` installed there. If not click on `Install` otherwise click on `Launch`

## Setup project
- Clone the repo by running the following command:
  > `git clone https://github.com/M3SOulu/TrendMiningPython.git`
- Open the cloned project in `VS Code` and also in the `CMD prompt` that you launced in previous setup
- Through the `CMD prompt`install required packages by running the following command in the root of this project.
  > `pip install -r requirements.txt`
- Once done you will be ready to Mine.

## Mining data

- Navigate into `Miners` directory.
- Pass the search parameters to the mining functions.
- Run the file by `python miner.py`.
- The mined and cleaned data will be, by default, saved to `Data` folder.

## Document-Term Matrix & Dendogram clustring

- Navigate into `Bow_DTM` directory
- Navigate into individual directories and run the files
- The graphs/images will be saved to Output folder and other information will be printed into console.
- Explore other methods in `DTM_class.py` file

## Word Clouds
- Navigate to the `Word_clouds` directory
- Navigate into individual directories and run the files
- The graphs/images will be saved to Output folder and other information will be printed into console.
- Explore other methods in `cloud_generator.py` file

## Timeline and Popularity
- Navigate to the `Timeline_and_popularity` directory
- Navigate into individual directories and run the files
- The graphs/images will be saved to Output folder and other information will be printed into console.
- Explore other methods in `timeline_and_popularity.py` file

## LDA
- Navigate to the `LDA` directory
- Navigate into individual directories and run the files
- The graphs/images will be saved to Output folder and other information will be printed into console.
- Explore other methods in `LDA.py` file
