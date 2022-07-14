import os

def createFile(file: str, path: str) -> None: 
    """This function is used to create the directory necessary to store the mined data.        

    Args:
        file (str): Name of the file to be created.
        path (str): Path of the directory where the files will be stored e.g. "../../Data".
    """
    does_folder_exist = os.path.exists(path)
    does_file_exist  = os.path.exists(path + '/' + file)
    if (does_folder_exist): 
        # Remove existing stack data file if already exist to add new one
        if (does_file_exist):
            print('Removing already existing',file,'file')
            os.remove(path + '/' + file)
        else:
            print( file + ' does not exist yet, ' + 'it will be downloaded')

    # Create Data folder if did not exist to store the csv file
    else: 
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        os.mkdir(root_dir+'/Data')
        print('Data folder created for csv file storage')
 