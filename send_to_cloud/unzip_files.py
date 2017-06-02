# put this file in the mnt/storage folder and then run
# to unzip all of the compressed comments data
import os

# this code was originally used to unzip 300GB+ of compressed files
# scrapped because now we are only using a subset and want to unzip
# only one folder
'''
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
'''

EXEC = "bzip2 -d "

for bz2 in os.listdir():
    print('WORKING ON ' + bz2)
    if '.bz2' in bz2:
        os.system(EXEC + bz2)
        print('FINISHED UNCOMPRESSING ' + bz2)
    else:
        print('DROPPED ' + bz2)

print('DONE')

