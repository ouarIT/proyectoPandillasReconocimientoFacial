
import os

def existe(path):
    isFile = os.path.isfile(path)
    if isFile:
        #print ('el '+ path +'archivo existe')
        return True
    else:
        print('el '+ path +'  no existe')
        return False




