
import re

def sanitise(data):
    return re.sub(r"\['|'\]|\[\"|\"\]|\\r|\\n", "", str(data))

def reviewToDict(*args):
    completeDict = {}
    values = []
    for arg in args:
        isString = isinstance(arg, str)
        if isString == True:
            key = arg
            continue
        for item in arg:
            if(isString == False):
                item = sanitise(item.contents)
                if item == "[]":
                    item = "null"
                values.append(item)
        if len(values) != 0:
            dictize = {key : values}
            completeDict.update(dictize)
    return completeDict

def makeDict(*args):
    adict = {}
    for arg in args:
        adict.update(arg)
    return adict