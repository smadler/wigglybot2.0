def getIngredients():
    result = {}
    with open("./data/cramomatic/ingredients.txt", 'r') as f:
        for line in f:
            items = line.split()
            if len(items) > 2:
                result[' '.join(items[:-2])] = {"Value": int(items[-1]), "Type": items[-2], "Name": ' '.join(items[:-2])}
    return result

def weightIngredients(result):
    with open("./data/cramomatic/ingredientweights.txt", 'r') as f:
        for line in f:
            items = line.split()
            if len(items) > 2:
                itemname = ' '.join(items[:-1])
                if itemname in result:
                    result[itemname]['Weight'] = int(items[-1])
    return result

def getResults():
    result = {}
    with open("./data/cramomatic/recipies.txt", 'r') as f:
        base = ''
        for line in f:
            line = line.strip()
            if base == '':
                base = line
                result[base] = []
            elif line == '----':
                base = ''
            else:
                result[base].append(line)                
    return result
