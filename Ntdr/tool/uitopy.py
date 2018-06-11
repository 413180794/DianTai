import glob
import os
import os.path
dir = 'UI'


# 遍历文件夹下所有的.ui文件并将其转换给.py文件
def listUiFile():
    list = []
    for file in glob.glob('../'+dir+'/'+'*.ui'):
        filename = os.path.splitext(file)[0].split('/')[2]
        filename = filename+'.ui'
        print(filename)
        list.append(filename)
    return list

def transPyFile(filename):
    return os.path.splitext(filename)[0] + '.py'


def runMain():
    list = listUiFile()
    for uiFile in list:
        pyfile = transPyFile(uiFile)
        cmd = 'pyuic5 -o ../UIPy/{pyfile} ../UI/{uifile}'.format(pyfile=pyfile,uifile=uiFile)
        os.system(cmd)


if __name__ == '__main__':
    runMain()
