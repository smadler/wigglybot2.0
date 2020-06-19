import discord
from discord.ext import commands
from discord.utils import get
from ..data.pokemon import Dens

class DenImager(commands.Cog):

    ### DICTIONARIES FOR ALL THE DENS AND THEIR SPECIES
    sword_den_dict = Dens.swordReg
    shield_den_dict = Dens.shieldReg
    sword_baby_den_dict = Dens.swordBaby
    shield_baby_den_dict = Dens.shieldBaby
    
    allowedsubs = {
        'Sh': 'Shield',
        'Sw': 'Sword',
        'Sheild': 'Shield',
        'Bb': 'Baby',
    }

    possibletops = [
        'Sword',
        'Shield',
        'Baby',
    ] 

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def den(self, ctx, *args):
        if not (get(ctx.message.author.roles, name="Max Host") or get(ctx.message.author.roles, name="Mods")):
            return
        
        argset = map(lambda w: self.allowedsubs[w] if w in self.allowedsubs else w,
                filter(lambda x: x in self.possibletops or str(x).isdigit() or x in self.allowedsubs,
                map(lambda y: y.capitalize(), args)))

        settings = {'sword': None, 'baby': False, 'den': None}

        for val in argset:
            if str(val).isdigit():
                settings['den'] = val
            elif val == 'Sword':
                settings['sword'] = True
            elif val == 'Shield':
                settings['sword'] = False
            elif val == 'Baby':
                settings['baby'] = True

        if settings['den'] == None:
            await ctx.send('Please specify a den.')
            return

        if settings['sword'] == None:
            await ctx.send('Please specify a version.')
            return

        await self.printDenList(ctx, settings['den'], settings['sword'], settings['baby'])
        
    async def printDenList(self, ctx, den:str, sword = True, babyden = False):
        if sword:
            if babyden:
                emoji_string = self.sword_baby_den_dict[den]
            else:
                emoji_string = self.sword_den_dict[den]
        else:
            if babyden:
                emoji_string = self.shield_baby_den_dict[den]
            else:
                emoji_string = self.shield_den_dict[den]
        await ctx.send(emoji_string)

def setup(bot):
    bot.add_cog(DenImager(bot))
