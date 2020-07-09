import discord
from discord.ext import commands
from discord.utils import get
from .utils import cramData
import re
import functools
import collections

class Cramomatic(commands.Cog):

    ### DICTIONARIES FOR ALL THE DATA NEEDED
    ingredients = cramData.getIngredients()
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
        

    @commands.command()
    async def recipe(self, ctx, *args):
        if not (ctx.channel.id == 647701301031075862 or get(ctx.message.author.roles, name="Max Host") or get(ctx.message.author.roles, name="Mods")):
            return

        composed = ' '.join(args)

        workingr = self.recipieregex.search(composed)

        if workingr == None:
            await ctx.send("I don't know how to make that.")
            return

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
            await ctx.send("%s is a special recipie with the core ingredient of %s." % (self.recipies[dataname][0][0], self.recipies[dataname][0][1]))
            return
            
        await ctx.send("%s can be made with the following ingredient combinations:\n%s" % (dataname, '\n'.join('A weight of %d with the %s sttribute.' % (self.expandValue(datanum), dataty) for dataty, datanum in self.recipies[dataname])))

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
            return (151, 1000) # 1000 is used as an arbitrarily large number
        if value == 0:
            return (0, 20)
        res = value * 10 + 11;
        return (res, res + 9)
    

def setup(bot):
    bot.add_cog(Cramomatic(bot))
