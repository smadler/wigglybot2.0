import json

class DataIO():

    def loadTypes():
        types_dict = {}
        with open("./data/pokemon/types2.txt", 'r') as f:
            for line in f:
                items = line.split('%')
                key, values = items[0], items[1:]
                types_dict[key] = values
        return types_dict

    def loadValuesGMAX():
        gm_dict = {}
        with open("./data/pokemon/valuesGMAX.txt", 'r') as f:
            for line in f:
                items = line.split('/')
                key, values = items[0], items[1:]
                gm_dict[key] = values
        return gm_dict

    def loadValues():
        norm_dict = {}
        with open("./data/pokemon/values.txt", 'r') as f:
            for line in f:
                items = line.split('/')
                key, values = items[0], items[1:]
                norm_dict[key] = values
        return norm_dict

    def loadPokeJSON():
        with open("./data/pokemon/pokemon.json", 'r') as f:
            poke_dict = json.load(f)
            return poke_dict

