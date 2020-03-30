import discord
from discord.ext import commands
from discord.utils import get
import random

class Wander(commands.Cog):

    sayings = [
	'<:wuggly:693973166477017240>', 
        '<a:wogglydance:693976658587287572>', 
        '<:wigglyyo:693973346240561222>', 
        '<:wigglywonder:692567051679694938>', 
        '<:wigglyspy:693973166678212738>', 
        '<a:wigglyspin:693983671396335798>',
        '<:wigglysmol:692600725850554388>',
        '<a:wigglyred:693983674567491604>',
        '<:wigglyhug:693973166350925885>',
        '<:wigglyhehe:693976765780983869>',
        '<:wigglydeepfried:692568022866722836>',
        '<:wigglydeeperfried:692567973579456573>',
        '<:reachingL:692568100973051925><:wigglycursed:692567625850552320><:reachingR:692568102491390004>', 
        '<:wigglybread:693974278747586650>',
        '<a:wigglyban:693973166112112741>', 
        '<:wiggly:692567118130053130>',
        '<:wiggluto:692567047434928158>',
        '<:space:686351664386801714>\n<:wigg1:692600720666525727><:wigg2:692600721282957343>\n<:wigg3:692600723992477716><:wigg4:692600723019530290>',
        '<:psyduckblush1:692567677897801729>', 
        '<:omegawiggly:693973165856260187>',
        '<:hyperomegawiggly:693973165457801296>', 
        '<:eyesack:692567491154804779>',
    ]

    sayweight = [
        17,
        4,
        8,
        9, 
        19, 
        15,
        10,
        20,
        2,
        16,
        14,
        3,
        3,
        18,
        11,
        22,
        7,
        1,
        5,
        6,
        3,
        12,
    ]

    channelPoss = []

    minsteps = 5
    stepvariance = 3
    steps = 0

    def __init__(self, bot):
        self.bot = bot
        self.steps = self.stepCounter()
        print('Initilized with '+self.steps+' steps')

    def stepCounter():
        return random.randrange(minsteps, minsteps + stepvariance)

    def getSaying():
        return random.choices(sayings, sayweight, k = 1)
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.channel not in self.channelPoss:
            self.channelPoss.append(message.channel)
        self.steps -= 1
        print(''+self.steps)
        if self.steps < 1:
            self.steps = self.stepCounter()
            target = random.choice(self.channelPoss)
            self.channelPoss = []
            await target.send(self.getSaying())

def setup(bot):
    bot.add_cog(PinManager(bot))
