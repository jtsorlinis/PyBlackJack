def getAction(playerval, dealerval, strategy):
    key = str(playerval) + "/" + str(dealerval)
    return strategy[key]

def readArray(file):
    file = open(file).read()
    array = []
    for row in file.split("\n"):
        array += [row.split(" ")]
    return array

def ArrayToDict(array):
    dict = {}
    for row in range(len(array)):
        for col in range(len(array[0])):
            if(row != 0 and col != 0):
                key = array[row][0] + "/" + array[0][col]
                dict[key] = array[row][col]
    return dict

def fileToDict(file):
    return ArrayToDict(readArray(file))
