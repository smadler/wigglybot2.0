import discord
from discord.ext import commands
from discord.utils import get

class PinManager(commands.Cog):

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

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        #Check if chn in whitelist
        if payload.channel_id not in allowedchn:
            return
        guild = await self.bot.fetch_guild(guild_id = payload.guild_id)
        member = await guild.fetch_member(member_id = payload.user_id)
        if payload.emoji.name == "📌" and get(member.roles, name = "Max Host"):
            channel = self.bot.get_channel(id = payload.channel_id)
            message = await channel.fetch_message(id = payload.message_id)
            await message.pin()

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        #Check if chn in whitelist
        if payload.channel_id not in allowedchn:
            return
        guild = await self.bot.fetch_guild(guild_id = payload.guild_id)
        member = await guild.fetch_member(member_id = payload.user_id)
        if payload.emoji.name == "📌" and get(member.roles, name = "Max Host"):
            channel = self.bot.get_channel(id = payload.channel_id)
            message = await channel.fetch_message(id = payload.message_id)
            await message.unpin()

def setup(bot):
    bot.add_cog(PinManager(bot))
