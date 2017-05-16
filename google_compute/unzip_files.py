# put this file in the mnt/storage folder and then run
# to unzip all of the compressed comments data
import os

folders = []
IGNORE = ['lost+found', 'unzip_files.py', '2006', '2010', '2009']
EXEC = "bzip2 -d "

for folder in os.listdir():
    if folder not in IGNORE:
        folders.append(folder)
print("DONE GETTING FOLDERS")
print(folders)

for folder in folders:
    print('CURRENTLY WORKING ON ' + folder)
    os.chdir(folder)
    print(os.getcwd())
    for bz2 in os.listdir():
        print('WORKING ON ' + bz2)
        os.system(EXEC + bz2)
        print('FINISHED UNCOMPRESSING ' + bz2)

    print('DONE WITH ' + folder + ' GOING BACK TO MAIN DIRECTORY')
    os.chdir('..')
    print('NOW BACK IN ' + os.getcwd())