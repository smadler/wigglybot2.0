import discord
from discord.ext import commands
from discord.utils import get
from .utils import cramData
import re
import functools
import collections
import random

class Cramomatic(commands.Cog):

    # Weighting Constants
    WEIGHTINGCONSTANT = 4
    MAXWEIGHT = 40

    ### DICTIONARIES FOR ALL THE DATA NEEDED
    ingredients = cramData.getIngredients()
    ingredients = cramData.weightIngredients(ingredients)
    ingredientsrw = cramData.getIngredients()
    ingredientsrw = cramData.weightIngredients(ingredients)
    recipies = collections.defaultdict(list)
    recipieindex = []
    pivotrec = cramData.getResults()
    specialvalues = {
            "Tiny Mushroom": "Big Mushroom",
            "Pearl": "Big Pearl",
            "Stardust": "Star Piece",
            "Big Mushroom": "Balm Mushroom",
            "Nugget": "Big Nugget",
            "Big Pearl": "Pearl String",
            "Star Piece": "Comet Shard",
            "Rare Candy": "Ability Capsule",
            "Bottle Cap": "Gold Bottle Cap",
        }

    def __init__(self, bot):
        self.bot = bot
        self.ingredienttokenizer = re.compile('|'.join('(?P<%s>%s)' % (re.sub('-', '__', re.sub(' ', '_', key)), key) for key in self.ingredients), re.I)

        for ctype, internallist in self.pivotrec.items():
            for cindex in range(len(internallist)):
                self.recipies[internallist[cindex]].append((ctype, cindex))
        for ing, resultant in self.specialvalues.items():
            self.recipies[resultant].append(('Special', ing))
        for key in self.recipies:
            self.recipieindex.append(key)
        self.recipieregex = re.compile('|'.join('(?P<K%d>%s)' % (key, self.recipieindex[key]) for key in range(len(self.recipieindex))), re.I)
        self.quanta = self.composequanta()
        while self.iteraterecipe():
            pass
        

    @commands.command()
    async def recipe(self, ctx, *args):
        if not (ctx.channel.id == 647701301031075862 or get(ctx.message.author.roles, name="Max Host") or get(ctx.message.author.roles, name="Mods")):
            return

        composed = ' '.join(args)

        workingr = self.recipieregex.search(composed)

        if workingr == None:
            await ctx.send("I don't know how to make that.")
            return

        dataname = self.recipieindex[int(workingr.lastgroup[1:])]
        data = self.recipies[dataname]

        target = random.choice(data)

        if target[0] == 'Special':
            await ctx.send("To make %s, toss `%s` into the Cram-O-Matic." % (dataname, target[1] + ', ' + random.choice(list(self.ingredients.keys())) + ', ' + target[1] + ', ' + target[1]))
            return

        resultant = self.findrecipe(4, [], 0, self.expandValue(target[1]), target[0])
        if resultant == None:
            resultant = ['ERROR, No Recipe found']

        await ctx.send("To make %s, toss `%s` into the Cram-O-Matic." % (dataname, ', '.join(resultant)))

    @commands.command()
    async def smartrecipe(self, ctx, *args):
        if not (ctx.channel.id == 647701301031075862 or get(ctx.message.author.roles, name="Max Host") or get(ctx.message.author.roles, name="Mods")):
            return

        composed = ' '.join(args)

        workingr = self.recipieregex.search(composed)

        if workingr == None:
            await ctx.send("I don't know how to make that.")
            return

        dataname = self.recipieindex[int(workingr.lastgroup[1:])]
        data = self.recipies[dataname]

        resultant = self.smartpicker(dataname, data)
        if resultant == None:
            resultant = [['ERROR, No Recipe found']]

        await ctx.send("To make %s, toss `%s` into the Cram-O-Matic." % (dataname, ', '.join(resultant[0])))

    #@commands.command()
   # async def rawsmartrecipe(self, ctx, *args):
        #if not (ctx.channel.id == 647701301031075862 or get(ctx.message.author.roles, name="Max Host") or get(ctx.message.author.roles, name="Mods")):
       #     return

      #  composed = ' '.join(args)
#
     #   workingr = self.recipieregex.search(composed)
#
    #    if workingr == None:
   #         await ctx.send("I don't know how to make that.")
  #          return
#
 #       dataname = self.recipieindex[int(workingr.lastgroup[1:])]
#        data = self.recipies[dataname]
#
        # Flip working dicionaries for the call
        #temp = self.ingredients
       # self.ingredients = self.ingredientsrw
      #  self.quanta = self.composequanta()
     #   resultant = self.smartpicker(dataname, data)
    #    self.ingredients = temp
   #     self.quanta = self.composequanta()
 #       
  #      if resultant == None:
 #           resultant = [['ERROR, No Recipe found']]
#
#        await ctx.send("To make %s, toss `%s` into the Cram-O-Matic." % (dataname, ', '.join(resultant[0])))

    @commands.command()
    async def recipeinfo(self, ctx, *args):
        if not (ctx.channel.id == 647701301031075862 or get(ctx.message.author.roles, name="Max Host") or get(ctx.message.author.roles, name="Mods")):
            return

        composed = ' '.join(args)

        workingr = self.recipieregex.search(composed)

        if workingr == None:
            await ctx.send("I don't know how to make that.")
            return

        dataname = self.recipieindex[int(workingr.lastgroup[1:])]

        if self.recipies[dataname][0][0] == 'Special':
            await ctx.send("%s is a special recipie with the core ingredient of %s." % (dataname, self.recipies[dataname][0][1]))
            return

        res = []
        for dataty, datanum in self.recipies[dataname]:
            res.append("A special recipie with the core ingredient of %s." % datanum if dataty == 'Special'
                            else 'A weight of %d to %d with the %s attribute.' % (self.expandValue(datanum)[0], self.expandValue(datanum)[1], dataty))
            
        await ctx.send("%s can be made with the following ingredient combination(s):\n%s" % (dataname, '\n'.join(res)))

    @commands.command()
    async def cram(self, ctx, *args):
        if not (ctx.channel.id == 647701301031075862 or get(ctx.message.author.roles, name="Max Host") or get(ctx.message.author.roles, name="Mods")):
            return
        
        composed = ' '.join(args)

        pot = []
        
        for ing in self.ingredienttokenizer.finditer(composed):
            pot.append(re.sub('_', ' ', re.sub('__', '-', ing.lastgroup)))

        print(len(pot))
        print(pot)

        if len(pot) > 4:
            await ctx.send("That's too many things.")
            return

        if len(pot) < 4:
            await ctx.send("I need more than that.")
            return

        if pot[0] in self.specialvalues and pot[0] == pot[2] and pot[0] == pot[3]:
            resu = self.specialvalues[pot[0]]
        else:
            rtype = self.ingredients[pot[0]]['Type']
            rvalue = functools.reduce(lambda a, x: a + self.ingredients[x]['Value'], pot, 0)

            resu = self.pivotrec[rtype][self.modulateValue(rvalue)] if rvalue > 0 else 'Pokeball'

        await ctx.send("If you toss `%s` in the Cram-O-Matic, you will recieve a %s." % (', '.join(pot), resu))

    @commands.command()
    async def itemdetails(self, ctx, *args):
        if not (ctx.channel.id == 647701301031075862 or get(ctx.message.author.roles, name="Max Host") or get(ctx.message.author.roles, name="Mods")):
            return
        
        composed = ' '.join(args)
        
        ing = self.ingredienttokenizer.search(composed)

        if ing == None:
            await ctx.send("I don't know what that is.")
            return
        
        item = re.sub('_', ' ', re.sub('__', '-', ing.lastgroup))

        await ctx.send("%s is a %s attribute item with a weight of %d." % (item, self.ingredients[item]['Type'], self.ingredients[item]['Value']))

    @commands.command()
    async def itemsubstitute(self, ctx, *args):
        if not (ctx.channel.id == 647701301031075862 or get(ctx.message.author.roles, name="Max Host") or get(ctx.message.author.roles, name="Mods")):
            return
        
        composed = ' '.join(args)
        
        ing = self.ingredienttokenizer.search(composed)

        if ing == None:
            await ctx.send("I don't know what that is.")
            return
        
        item = re.sub('_', ' ', re.sub('__', '-', ing.lastgroup))

        await ctx.send("You use %s (%s) as a replacement for any of the following:\n%s" % (item, self.ingredients[item]['Type'],
                                '\n'.join('%s (%s)' % (poss['Name'], poss['Type']) for poss in self.find(self.ingredients[item]['Value'],
                                self.ingredients[item]['Value'], None, [item]))))

    def modulateValue(self, value: int):
        if value < 1:
            return None
        if value < 21:
            return 0
        if value < 31:
            return 1
        if value < 41:
            return 2
        if value < 51:
            return 3
        if value < 61:
            return 4
        if value < 71:
            return 5
        if value < 81:
            return 6
        if value < 91:
            return 7
        if value < 101:
            return 8
        if value < 111:
            return 9
        if value < 121:
            return 10
        if value < 131:
            return 11
        if value < 141:
            return 12
        if value < 151:
            return 13
        return 14

    def expandValue(self, value: int):
        if value > 14 or value < 0:
            return None
        if value == 14:
            return (151, 255) # 255 is used as an arbitrarily large number
        if value == 0:
            return (0, 20)
        res = value * 10 + 11;
        return (res, res + 9)

    def findrecipe(self, remaininging: int, inglist, currentweight: int, weighttarget, nature = None):
        if remaininging < 1: # Should not happen
            return None
        
        minweight = weighttarget[0] - currentweight if remaininging == 1 else 0
        maxweight = weighttarget[1] - currentweight

        while not minweight > maxweight:
            if remaininging == 1 and inglist[0] in self.specialvalues and inglist[0] == inglist[2]:
                prohibits = inglist[0]
            else:
                prohibits = None            
            selectfrom = self.find(minweight, maxweight, nature, [prohibits])
            if selectfrom == []:
                return None
            select = random.choice(selectfrom)
            currw = select['Value'] + currentweight
            tempings = inglist[:]
            tempings.append(select['Name'])
            
            if remaininging == 1: # Base Case
                if currw > weighttarget[1] or currw < weighttarget[0]: # Double check, neither should be the case
                    return None
                return tempings

            possibleres = self.findrecipe(remaininging - 1, tempings, currw, weighttarget)

            if possibleres != None: # Found a set of values that works
                return possibleres

            # Value found was too low
            minweight = select['Value'] + 1
            
        return None # No value was big enough to work

    def find(self, minweight, maxweight, nature = None, prohibits = [], allowableweight = None): # Returns a list of dicts corrosponding to the given restrictions
        res = []
        #print(minweight, maxweight, nature, prohibits, allowableweight)
        
        for possibility in self.ingredients.values():
            if nature != None and possibility['Type'] != nature:
                continue
            if allowableweight != None:
                if not 'Weight' in possibility or possibility['Weight'] > allowableweight:
                    continue
            if possibility['Name'] in prohibits:
                continue
            if possibility['Value'] > maxweight or possibility['Value'] < minweight:
                continue
            res.append(possibility)

        #print(res)
        return res

    # composeLists takes a list of prohibited words and a max quantum, then returns a list of
    # values and a list of delimiters for where the values delimters are
    # the values list is a list of itemvalues per weight, split by quantum weights according to
    # the delimiter list in marks
    def composeLists(self, prohibited, quantum, nature = None):
        temp = collections.defaultdict(list) # A bucketsort of sorts for this. Keys are weights
        vals, marks = [], [0]

        for item in self.find(0, 255, nature, prohibited, quantum):
            if item['Value'] not in temp[item['Weight']]:
                temp[item['Weight']].append(item['Value'])

        for quant in self.quanta:
            if quant > quantum:
                break
            random.shuffle(temp[quant])
            for ap in temp[quant]:
                if ap not in vals:
                    vals.append(ap)
            marks.append(len(vals))
        
        return (vals, marks)

    def composequanta(self):
        res = []
        for item in self.ingredients.values():
            if item['Weight'] not in res:
                res.append(item['Weight'])
        res.sort()
        return res

    def iteraterecipe(self):
        newvals = {}
        for recipename in self.recipies:
            name = "Kings Rock" if recipename == "King's Rock" else recipename
            if name in self.ingredients:
                xx = self.smartpicker(recipename, self.recipies[recipename], self.ingredients[name]['Weight'] - (self.WEIGHTINGCONSTANT + 1))
                if xx != None:
                    newvals[name] = xx[1] + self.WEIGHTINGCONSTANT
        for key, val in newvals.items():
            self.ingredients[key]['Weight'] = val
            
        self.quanta = self.composequanta()
        
        if newvals == {}:
            return False
        return True

    def smartpicker(self, recipename, recipes, minweight = 300000):
        res = []
        spec = None

        for recipe in recipes:
            if recipe[0] == 'Special': # Deal with special recipes
                if self.ingredients[recipe[1]]['Weight'] > minweight:
                    continue
                randing = random.choice(self.find(0, 255, None, [recipename], self.quanta[0]))['Name']
                possw = self.ingredients[recipe[1]]['Weight']
                if possw < minweight:
                    minweight = possw
                    res = []
                res.append([recipe[1], randing, recipe[1], recipe[1]])
                spec = recipe[1]
                continue

            # Deal with non-special recipes
            resultant = self.smartfindrecipe(self.expandValue(recipe[1]), recipe[0], [recipename] if recipename != "King's Rock" else ["Kings Rock"], minweight)
            if resultant != None:
                possw = max(resultant[0][0], resultant[1][0], resultant[2][0], resultant[3][0])
                if possw < minweight:
                    minweight = possw
                    res = []
                resultant[0] = (resultant[0][0], resultant[0][1], recipe[0])
                res.append(resultant)

        if res == []:
            res = None
        else:
            res = random.choice(res)
        if res == None:
            return None

        if res[0] == spec:
            return (res, minweight)

        res[0] = random.choice(self.find(res[0][1], res[0][1], res[0][2], [recipename], res[0][0]))['Name']
        res[1] = random.choice(self.find(res[1][1], res[1][1], None, [recipename], res[1][0]))['Name']
        res[2] = random.choice(self.find(res[2][1], res[2][1], None, [recipename], res[2][0]))['Name']
        if res[0] in self.specialvalues and res[0] == res[2]:
            prohibits = [recipename, res[0]]
        else:
            prohibits = [recipename]
        attempt = self.find(res[3][1], res[3][1], None, prohibits, res[3][0])
        while attempt == []:
            attempt = self.find(res[3][1], res[3][1], None, prohibits, self.quanta[self.findindex(self.quanta, res[3][0]) + 1])
        res[3] = random.choice(attempt)['Name']
            
        return (res, minweight)
    
    #returns a series of quantumweight/itemweight tuples
    def smartfindrecipe(self, weighttarget, nature, prohibited = [], quantum = 300000):
        vals, marks = self.composeLists(prohibited, quantum)
        startvals, startmarks = self.composeLists(prohibited, quantum, nature) # also takes an additional optional nature

        for quantaindex in range(len(marks)-1): # The length of marks will always be the allowed number of quanta plus one
            if marks[quantaindex] == marks[quantaindex + 1]:
                continue # Trim time by ignoring quanta that don't have any new associated values
            
            for firstvalindex in range(startmarks[quantaindex + 1]): # check every beginning each deepening
                
                firstval = startvals[firstvalindex]
                if firstval > weighttarget[1] or firstval < weighttarget[0] - 3 * self.MAXWEIGHT: # Trim impossible values early
                    continue
                
                for val2index in range(marks[quantaindex], marks[quantaindex + 1]):
                    secondval = vals[val2index]
                    if secondval + firstval > weighttarget[1] or secondval < weighttarget[0] - (firstval + 2 * self.MAXWEIGHT): # Trim impossible values
                        continue
                       
                    for val3index in range(marks[quantaindex + 1]):
                        thirdval = vals[val3index]
                        if thirdval + secondval + firstval > weighttarget[1] or thirdval < weighttarget[0] - (firstval + secondval + self.MAXWEIGHT): # Trim impossible values
                            continue
                    
                        for val4index in range(val3index, marks[quantaindex + 1]):
                            fourthval = vals[val4index]
                            if fourthval + thirdval + secondval + firstval > weighttarget[1] or firstval + secondval + thirdval + fourthval < weighttarget[0]: # Trim impossible values
                                continue

                            # If here, the 4 values fit the criteria
                            return [(self.quanta[self.findindex(startmarks, firstvalindex)], firstval), (self.quanta[quantaindex], secondval),
                                    (self.quanta[self.findindex(marks, val3index)], thirdval), (self.quanta[self.findindex(marks, val4index)], fourthval)]

        return None # No such recipe exists, should not be called unless quantum is set

    # Takes a marklist and the index and returns which index range in that list the indexval associates with
    def findindex(self, marklist, indexval):
        for res in range(len(marklist) - 1):
            if indexval < marklist[res + 1]:
                return res
        

def setup(bot):
    bot.add_cog(Cramomatic(bot))
