
with open('IP.config') as IPtxt:
    print(str(IPtxt.read().split("=")[1]))