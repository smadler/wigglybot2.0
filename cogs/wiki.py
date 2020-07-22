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

    @commands.command()
    async def rng(self, ctx):
        await ctx.send("<https://www.reddit.com/r/pokemonmaxraids/comments/esv23y/the_pokemon_swsh_raid_rng_manipulation_guide/>")

    @commands.command()
    async def fancy(self, ctx):
        await ctx.send("<https://www.reddit.com/r/pokemonmaxraids/wiki/formatting>")

def setup(bot):
    bot.add_cog(Wiki(bot))
