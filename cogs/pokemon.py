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

    # TODO: Make this part more configurable, especially on the fly
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

    serverid = 645011176182251522

    fullpermchn = 647701301031075862
    # End
    
    types_dict = DataIO.loadTypes()
    gm_dict = DataIO.loadValuesGMAX()
    norm_dict = DataIO.loadValues()
    poke_dict = DataIO.loadPokeJSON()

    allowedsubs = {
        'Building': 'Duraludon',
        'Sky Egg': 'Togekiss',
        'Cake': 'Alcremie',
        'Alcreamie': 'Alcremie',
        'Sheild': 'Shield',
    }

    possibletops = [
        'Promo',
        'Sword',
        'Shield',
        'Clear',
        'G',
        'Gmax',
    ] 

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
    async def namerater(self, ctx, arg1: str):
        if ctx.channel.id not in self.allowedchn:
            return
        if get(ctx.message.author.roles, name="Max Host") or get(ctx.message.author.roles, name="Mods"):
            await ctx.channel.edit(name = arg1)

    @commands.command()      
    async def topic(self, ctx, *args):
        if ctx.channel.id not in self.allowedchn:
            return
        
        if get(ctx.message.author.roles, name="Max Host") or get(ctx.message.author.roles, name="Mods"):
            # Verify that the topic is a name or den number
            newtopic = None

            if args == ():
                newtopic = ''

            else:
                argset = map(lambda w: self.allowedsubs[w] if w in self.allowedsubs else w, filter(lambda x: x in self.possibletops or x in self.norm_dict or str(x).isdigit(),
                            list(map(lambda y: y.capitalize(), args)) + list(map(lambda z, q: z.capitalize() + ' ' + q.capitalize(), ['l'] + list(args), args))))

                settings = {'clear': False, 'num': None, 'game': None, 'promo': False, 'species': None, 'gmax': False}

                for var in argset:
                    if str(var).isdigit():
                        settings['num'] = var
                    elif var == 'Shield' or var == 'Sword':
                        settings['game'] = var
                    elif var == 'Promo':
                        settings['promo'] = True
                    elif var == 'G' or var == 'Gmax':
                        settings['gmax'] = True
                    elif var == 'Clear':
                        settings['clear'] = True

                if settings['clear']:
                    newtopic = ''
                elif settings['num'] != None:
                    newtopic = 'Now hosting: '
                    if settings['game']:
                        newtopic = newtopic + settings['game'] + ' '
                    newtopic = newtopic + 'Den ' + settings['num']
                elif settings['promo']:
                    newtopic = 'Now hosting: '
                    if settings['game']:
                        newtopic = newtopic + settings['game'] + ' '
                    newtopic = newtopic + 'Promo Den'
                elif settings['species']:
                    newtopic = 'Now hosting: '
                    if settings['gmax']:
                        newtopic = newtopic + 'GMax '
                    newtopic = newtopic + settings['species']
                
            if newtopic != None:
                await ctx.channel.edit(topic = newtopic)

    @commands.command()
    async def ball(self, ctx, arg1 = None, arg2 = None):
        if not (ctx.channel.id == self.fullpermchn or get(ctx.message.author.roles, name="Max Host") or get(ctx.message.author.roles, name="Mods")):
            return
        
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
        await ctx.send(embed = embed)


    @commands.command()
    async def matchup(self, ctx, arg1 = None, arg2 = None):
        if not (ctx.channel.id == self.fullpermchn or get(ctx.message.author.roles, name="Max Host") or get(ctx.message.author.roles, name="Mods")):
            return

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
    async def wiggly(self, ctx, arg1: int = None, *args):
        if get(ctx.message.author.roles, name="Mods"):
            target = ctx.bot.get_channel(arg1)
            if target == None:
                await ctx.send('Channel not found.')
                return
            await target.send(' '.join(args))
            await ctx.send('Message sent.')
            return
        else:
            await ctx.send(file = File('./data/pokemon/wiggly.png'))

    @commands.command()
    async def info(self, ctx, arg1: str):
        if not (ctx.channel.id == self.fullpermchn or get(ctx.message.author.roles, name="Max Host") or get(ctx.message.author.roles, name="Mods")):
            return

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
