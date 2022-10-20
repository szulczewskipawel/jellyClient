from prettytable import PrettyTable

def printPrettyTable(data):
    i = 0
    for z in data:
        if i == 0:
            z.insert(0, "Lp")
        else:
            z.insert(0, i)
        i += 1
    tab = PrettyTable(data[0])
    tab.add_rows(data[1:])
    print(tab)

def showBufferOrPlaylist(buforplay):
    if len(buforplay) > 0:
        bList = [["Name"]]
        for i in buforplay:
            smList = list()
            smList.append(buforplay[i][0])
            bList.append(smList)
        printPrettyTable(bList)
    else:
        print('The list is empty at this momment.')

