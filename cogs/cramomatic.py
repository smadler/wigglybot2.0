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

    ### DICTIONARIES FOR ALL THE DATA NEEDED
    ingredients = cramData.getIngredients()
    cramData.weightIngredients(ingredients)
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
            resultant = ['ERROR, No Recipe found']

        await ctx.send("To make %s, toss `%s` into the Cram-O-Matic." % (dataname, ', '.join(resultant[0])))

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
            
        await ctx.send("%s can be made with the following ingredient combination(s):\n%s" % (dataname, '\n'.join('A weight of %d to %d with the %s attribute.' %
                                                (self.expandValue(datanum)[0], self.expandValue(datanum)[1], dataty) for dataty, datanum in self.recipies[dataname])))

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

        await ctx.send("You use %s as a replacement for any of the following:\n%s" % (item,
                                '\n'.join(poss['Name'] for poss in self.find(self.ingredients[item]['Value'], self.ingredients[item]['Value'], None, [item]))))

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

        return res

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
            name = "Kings Rock" if name == "King's Rock" else recipename
            if name in self.ingredients:
                xx = self.smartpicker(recipename, self.recipies[recipename], self.ingredients[name] - 1)
                if xx != None:
                    newvals[name] = xx[1] + self.WEIGHTINGCONSTANT
        for key, val in newvals.items():
            self.ingredients[key]['Weight'] = val
        self.quanta = self.composequanta()
        if newvals == {}:
            return False
        return True

    def smartpicker(self, recipename, recipes, weightlimit = 300000):
        minweight = weightlimit
        res = None

        for recipe in recipes:
            if recipe[0] == 'Special':
                randing = random.choice(self.find(0, 255, None, [recipename], self.quanta[0]))['Name']
                return ([recipe[1], randing, recipe[1], recipe[1]], self.ingredients[recipe[1]['Weight']])
            for quantum in self.quanta:
                if quantum >= minweight:
                    break
                resultant = self.smartfindrecipe(4, [], 0, self.expandValue(recipe[1]), recipe[0], [recipename] if recipename != "King's Rock" else ["Kings Rock"], quantum)
                if resultant != None:
                    res = resultant
                    minweight = quantum
                    break

        if res == None:
            return None
        return (res, quantum)
    
    def smartfindrecipe(self, remaininging: int, inglist, currentweight: int, weighttarget, nature = None, prohibited, quantum):
        if remaininging < 1: # Should not happen
            return None
        
        minweight = weighttarget[0] - currentweight if remaininging == 1 else 0
        maxweight = weighttarget[1] - currentweight

        for quantumm in self.quanta:
            if quantumm > quantum:
                return None
            while not minweight > maxweight:
                if remaininging == 1 and inglist[0] in self.specialvalues and inglist[0] == inglist[2]:
                    prohibits = [inglist[0]]
                else:
                    prohibits = []
                prohibits.extend(prohibited)
                selectfrom = self.find(minweight, maxweight, nature, prohibits, quantumm)
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

                possibleres = self.smartfindrecipe(remaininging - 1, tempings, currw, weighttarget, prohibited, quantum)

                if possibleres != None: # Found a set of values that works
                    return possibleres

                # Value found was too low
                minweight = select['Value'] + 1
            
        return None # No value was big enough to work
    

def setup(bot):
    bot.add_cog(Cramomatic(bot))
