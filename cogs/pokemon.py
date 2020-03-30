import discord
from .utils.dataIO import DataIO
from discord.ext import commands
import urllib.request
from discord.utils import get
import re
import traceback

class Pokemon(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    allowedchn = [
	646049007998730290,
	646053591462707260,
	646053662833246239,
	665613353397518396,
	666833127448117280,
	666834649506644008,
	668148156504211476,
	669359745114570795,
	670457916339388446,
	670459024755523584,
	669361675560026167,
	673012289120632846,
	668360850750308358,
    ]

    types_dict = DataIO.loadTypes()
    gm_dict = DataIO.loadValuesGMAX()
    norm_dict = DataIO.loadValues()
    poke_dict = DataIO.loadPokeJSON()

    isemoji = re.compile(r'<a?:.*:[0987654321]+>')
    isbaseemoji = re.compile(r':.*:')
    extract = re.compile(r'(?<=:)[0987654321]+(?=[>])')

    @commands.command()      
    async def narnerater(self, ctx, arg1: str):
        if ctx.channel.id not in self.allowedchn:
            return
        if get(ctx.message.author.roles, name="Max Host") or get(ctx.message.author.roles, name="Mods"):
            arg1 = re.sub('m', 'rn', arg1)
            if arg1 == 'roorn-12':
                arg1 = 'room-12'
            await ctx.channel.edit(name = arg1)

    @commands.command()      
    async def topic(self, ctx, arg1 = None, arg2 = None):
        if ctx.channel.id not in self.allowedchn:
            return
        if get(ctx.message.author.roles, name="Max Host") or get(ctx.message.author.roles, name="Mods"):
            # Verify that the topic is a name or den number
            newtopic = None

            if arg1 == None or arg1.capitalize() == 'Clear':
                newtopic = ''
                
            elif str(arg1).isdigit() or arg1.capitalize() == 'Promo':
                pk = ' '
                
                if arg2 != None and arg2.capitalize() == 'Sword':
                   pk = ' Sword '
                elif arg2 != None and arg2.capitalize() == 'Shield':
                   pk = ' Shield '
                   
                newtopic = 'Now hosting:' + pk + 'Den ' + str(arg1).capitalize()
                
            elif arg2 != None and (str(arg2).isdigit() or arg2.capitalize() == 'Promo'):
                pk = ' '
                
                if arg1.capitalize() == 'Sword':
                   pk = ' Sword '
                elif arg1.capitalize() == 'Shield':
                   pk = ' Shield '
                   
                newtopic = 'Now hosting:' + pk + 'Den ' + str(arg2).capitalize()
                
            #one word name
            elif arg1 != None and arg2 == None:
                pk = arg1.capitalize()                

                if pk in self.norm_dict:
                    newtopic = 'Now hosting: ' + pk

            #Check GMax
            elif arg1 == 'g' or arg1 == 'G' and arg2 != None:
                pk = arg2.capitalize()

                if pk in self.gm_dict:
                    newtopic = 'Now hosting: GMax ' + pk

            else: #try reading as a 2 word name
                pk = arg1.capitalize() + ' ' + arg2.capitalize()

                if pk in self.norm_dict:
                    newtopic = 'Now hosting: ' + pk

            if newtopic != None:
                await ctx.channel.edit(topic = newtopic)

    @commands.command()
    async def ball(self, ctx, arg1 = None, arg2 = None):
        if arg1 == None:
            msg = ('Invalid input!')

        #one word name
        elif arg1 != None and arg2 == None:
            pk = arg1.capitalize()

            if pk not in self.norm_dict:
                msg = "Pokemon not found!"

            else:
              msg = '\n'.join(map(str, self.norm_dict.get(pk)))

        #Check GMax
        elif arg1 == 'g' or arg1 == 'G' and arg2 != None:
            pk = arg2.capitalize()

            if pk not in self.gm_dict:
                msg="Pokemon not found!"

            else:
                msg = '\n'.join(map(str, self.gm_dict.get(pk)))

        else: #try reading as a 2 word name
            pk = arg1.capitalize() + ' ' + arg2.capitalize()

            if pk not in self.norm_dict:
                msg="Pokemon not found!"

            else:
                msg = '\n'.join(map(str, self.norm_dict.get(pk)))

        embed = discord.Embed()
        embed.title = pk
        embed.set_footer(text = 'Please note these values may not be completely correct!')
        embed.add_field(name = 'Catch Rates', value = msg)
        await ctx.send('Just use a Repeat Ball.')
        if not ctx.author.dm_channel:
            await ctx.author.create_dm()
        await ctx.author.dm_channel.send(embed = embed)


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

        await ctx.send("Don't bother me, I'm on holiday.")


    @commands.command()
    async def wiggly(self, ctx, arg1: int, *args):
        if get(ctx.message.author.roles, name="Mods"):
            target = ctx.bot.get_channel(arg1)
            if target == None:
                await ctx.send('Channel not found.')
                return
            await target.send(' '.join(args))
            await ctx.send('Message sent.')
            return

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

            await ctx.send('Not worth my time.')

    @commands.command()
    async def vote(self, ctx, *args):
        emoji = list(filter(lambda x: self.isemoji.match(x) or self.isbaseemoji.match(x), args))

        if emoji == []:
            emoji = [':thumbsup:',':thumbsdown:']

        for emoj in emoji:
            try:
                if self.isbaseemoji.match(emoj):
                    #Add support for non thumbs later
                    if emoj == ':thumbsup:':
                        await ctx.message.add_reaction(u"\U0001F44D")
                    elif emoj == ':thumbsdown:':
                        await ctx.message.add_reaction(u"\U0001F44E")                        
                else:
                    reactid = int(self.extract.search(emoj).group(0))
                    reaction = self.bot.get_emoji(reactid)
                    await ctx.message.add_reaction(reaction)
            except:
                traceback.print_exc()

def setup(bot):
    bot.add_cog(Pokemon(bot))
