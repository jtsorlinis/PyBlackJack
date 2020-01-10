def readArray(file):
    file = open(file).read()
    array = []
    for row in file.split("\n"):
        array += [row.split(" ")]
    return array
