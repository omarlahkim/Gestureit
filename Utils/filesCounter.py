import os




def filesCounter(path):
    nbFiles = 0
    nbDirectories=0
    for base, dirs, files in os.walk(path):
        for directories in dirs:
            nbDirectories += 1
        for Files in files:
            nbFiles += 1
    return (nbFiles,nbDirectories)
