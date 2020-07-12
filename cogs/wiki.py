import discord
from discord.ext import commands

# Only split into its own gear for easier %help
class Wiki(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def raidiquette(self, ctx):
        await ctx.send("<https://www.reddit.com/r/pokemonmaxraids/wiki/raidetiquette>")

    @commands.command()
    async def faq(self, ctx):
        await ctx.send("<https://www.reddit.com/r/pokemonmaxraids/wiki/faq>")
        
    @commands.command()
    async def raidfaq(self, ctx):
        await ctx.send("<https://www.reddit.com/r/pokemonmaxraids/wiki/raidfaq>")
        
    @commands.command()
    async def flairs(self, ctx):
        await ctx.send("<https://www.reddit.com/r/pokemonmaxraids/wiki/flairlevels>")
        

def setup(bot):
    bot.add_cog(Wiki(bot))
