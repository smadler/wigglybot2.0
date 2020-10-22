import json

class DataIO:

    def loadTypes(self):
        types_dict = {}
        with open("./data/pokemon/types2.txt", 'r') as f:
            for line in f:
                items = line.split('%')
                key, values = items[0], items[1:]
                types_dict[key] = values
        return types_dict

    def loadValuesGMAX(self):
        gm_dict = {}
        with open("./data/pokemon/valuesGMAX.txt", 'r') as f:
            for line in f:
                items = line.split('/')
                key, values = items[0], items[1:]
                gm_dict[key] = values
        return gm_dict

    def loadValues(self):
        norm_dict = {}
        with open("./data/pokemon/pokemon_full.json", 'r') as f:
            temp = json.load(f)
        norm_dict = []
        for item in temp:
            norm_dict.append(self.getCatchRates(item))
        return norm_dict

    def loadPokeJSON(self):
        with open("./data/pokemon/pokemon.json", 'r') as f:
            poke_dict = json.load(f)
            return poke_dict

    def  getCatchRates(self, species):
        # find the normalcatchrate first
        normalrate = species["catch"] / 1.0
         
        # create the array 
        arr = [
                3.5 * normalrate,
                3 * normalrate,
                2 * normalrate,
                1.5 * normalrate,
                3.5 * normalrate if 'Water' in species["types"] or 'Bug' in species["types"] else normalrate,
                2 * normalrate,
                4 * normalrate if species["base_speed"] > 100 else normalrate,
                0.1 * normalrate,
                normalrate,
              ]

        # Calc from catchrates
        for x in range(len(arr)):
            arr[x] = (arr[x] / 255) ** 0.75
            arr[x] = arr[x] * 100
            arr[x] = 100 if arr[x] >= 100 else arr[x]

        # Assemble the text
        arr = [
                "Repeat: %.1f%%" % arr[0],
                "Dusk: %.1f%%" % arr[1],
                "Ultra: %.1f%%" % arr[2],
                "Great: %.1f%%" % arr[3],
                "Net: %.1f%%" % arr[4],
                "Level: %.1f%% (Optimal Conditions)" % arr[5],
                "Fast: %.1f%%" % arr[6],
                "Beast: %.1f%%" % arr[7],
                "All others: %.1f%%" % arr[8],
              ]

        return (species["name"], arr)

