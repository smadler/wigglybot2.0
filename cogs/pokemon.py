import discord
from .utils.dataIO import DataIO
from discord.ext import commands
import urllib.request
from discord.utils import get

class Pokemon(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    types_dict = DataIO.loadTypes()
    gm_dict = DataIO.loadValuesGMAX()
    norm_dict = DataIO.loadValues()
    poke_dict = DataIO.loadPokeJSON()


    @commands.command()      
    async def namerater(self, ctx, arg1: str):
        if get(ctx.message.author.roles, name="Max Host") or get(ctx.message.author.roles, name="Mods"):
            await ctx.channel.edit(name = arg1)

    @commands.command()
    async def ball(self, ctx, arg1 = None, arg2 = None):
        if arg1 == None:
            msg = ('Invalid input!')

        elif arg1 != None and arg2 == None:
            pk = arg1.capitalize()

            if pk not in self.norm_dict:
                msg = "Pokemon not found!"

            else:
              msg = '\n'.join(map(str, self.norm_dict.get(pk)))

        elif arg1 == 'g' or arg1 == 'G' and arg2 != None:
            pk = arg2.capitalize()

            if pk not in self.gm_dict:
                msg="Pokemon not found!"

            else:
                msg = '\n'.join(map(str, self.gm_dict.get(pk)))

        embed = discord.Embed()
        embed.title = pk
        embed.set_footer(text = 'Please note these values may not be completely correct!')
        embed.add_field(name = 'Catch Rates', value = msg)
        await ctx.send(embed = embed)


    @commands.command()
    async def matchup(self, ctx, arg1 = None, arg2 = None):
        if arg1 == None:
            msg = ('Invalid input!')

        else:
            msg=""
            if arg2==None:
                #no 2nd argument
                types=arg1.split("/")
                if len(types)==1:
                    ptype =str(types[0].capitalize())
                    ptype+="/"+str(types[0].capitalize())
                else:
                    ptype = str(types[0].capitalize())
                    ptype+="/"+str(types[1].capitalize())
            else:
                ptype = str(arg1.capitalize())
                ptype+="/"+str(arg2.capitalize())

            if (ptype not in self.types_dict):
                msg += "Invalid input!"

            else:
                msg+=' For ' + str(ptype) +' types, use '
                msg+='\n'.join(map(str, self.types_dict.get(ptype))).rstrip()
                msg+=' type moves!'

        await ctx.send(msg)


    @commands.command()
    async def wiggly(self, ctx):
        await ctx.send(file = File('./data/pokemon/wiggly.png'))

    @commands.command()
    async def info(self, ctx, arg1: str):
        poke = None
        for p in self.poke_dict:
            if p['name'] == arg1.capitalize():
                poke = p
                break
        
        if poke == None:
            await ctx.send('Pokemon not found')
        else:
            embed = discord.Embed()
            embed.title = poke['name']
            embed.description = poke['description']

            if p['galar_dex'] == 'foreign':
                embed.add_field(name = 'Galar Pokedex ID', value = "Not in Galar", inline=False)
            else:
                embed.add_field(name = 'Galar Pokedex ID', value = p['galar_dex'], inline=False)

            abilities = ''
            for a in p['abilities']:
                if abilities == a + '\n':
                    pass
                else:
                    abilities += a + '\n'

            types = ''
            for t in p['types']:
                if types == t + '\n':
                    pass
                else:
                    types += t + '\n'

            embed.add_field(name = 'Type(s)', value = types, inline=False)
            embed.add_field(name = 'Abilities', value = abilities, inline=False)

            await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Pokemon(bot))
