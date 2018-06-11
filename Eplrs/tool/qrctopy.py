import sys

import os


while True:
    print("请输入qrc文件名")
    qrcfilename = str(input())
    print("请输入py文件名")
    pyfilename = str(input())
    if not qrcfilename.endswith('.qrc'):
        print("qrc文件格式错误，请重新输入")
        continue
    if not pyfilename.endswith('.py'):
        print("py文件格式错误，请重新出入")
        continue
    try:
        cmd = 'pyrcc5  ../resource/{qrcfile} -o {pyfile}'.format(qrcfile=qrcfilename, pyfile=pyfilename)
        os.system(cmd)
        print("成功运行")
        break
    except:
        print("文件不存在")
