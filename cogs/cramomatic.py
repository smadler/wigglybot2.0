import discord
from discord.ext import commands
from discord.utils import get
from .utils import cramData
import re
import functools

class Cramomatic(commands.Cog):

    ### DICTIONARIES FOR ALL THE DATA NEEDED
    ingredients = cramData.getIngredients()
    #recipies = {}
    povotrec = cramData.getResults()

    def __init__(self, bot):
        self.bot = bot
        self.ingredienttokenizer = re.compile('|'.join('(?P<%s>%s)' % (key, key) for key in ingredients), re.I)
        #self.reciperegex = re.compile('|'.join('(?P<%s>%s)' % (key, key) for key in recipies), re.I)
        

 #   @commands.command()
#    async def recipie(self, ctx, *args):
  #      if not (ctx.channel.id == 647701301031075862 or get(ctx.message.author.roles, name="Max Host") or get(ctx.message.author.roles, name="Mods")):
   #         return
#
    #    composed = ' '.join(args)
#
     #   workingr = self.recipieregex.search(composed)
#
      #  if workingr == None:
       #     await ctx.send("I don't know how to make that.")
        #    return


    @commands.command()
    async def cram(self, ctx, *args):
        if not (ctx.channel.id == 647701301031075862 or get(ctx.message.author.roles, name="Max Host") or get(ctx.message.author.roles, name="Mods")):
            return
        
        composed = ' '.join(args)

        pot = []
        
        for ing in self.ingredienttokenizer.finditer(composed):
            pot.append(ing.lastgroup)

        if len(pot) > 4:
            await ctx.send("That's too many things.")
            return

        if len(pot) < 4:
            await ctx.send("I need more than that.")
            return
      
        rtype = ingredients[pot[0]]['Type']
        rvalue = functools.reduce(lambda a, b: a+b, map(lambda x: ingredients[x]['Value'], pot))

        resu = pivotrec[rtype][self.modulateValue(rvalue)] if rvalue > 0 else 'Pokeball'

        await ctx.send("If you toss `%s` in the Cram-O-Matic, you will recieve a %s" % (', '.join(pot), resu))


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
    

def setup(bot):
    bot.add_cog(Cramomatic(bot))
