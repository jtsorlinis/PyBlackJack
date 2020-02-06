def getAction(playerval, dealerval, strategy):
    key = ((playerval + dealerval) * (playerval + dealerval + 1))/ 2 + dealerval
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
        playerval = int(array[row][0])
        for col in range(len(array[0])):
            dealerval = int(array[0][col])
            if(row != 0 and col != 0):
                key = ((playerval + dealerval) * (playerval + dealerval + 1))/ 2 + dealerval
                dict[key] = array[row][col]
    return dict

def fileToDict(file):
    return ArrayToDict(readArray(file))
