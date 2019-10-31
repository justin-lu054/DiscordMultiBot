import discord
from discord.ext import commands
import asyncio 
import datetime

class CockAndBallCog(commands.Cog, name = "CockAndBall"):
    def __init__(self, bot):
        self.bot = bot 

    @commands.command()
    async def cock_and_ball(self, ctx):
        wikipedia = "Cock and ball torture (CBT), penis torture or dick torture is a sexual activity involving application of pain or constriction to the penis or testicles."
        await ctx.send(wikipedia)
    
    @commands.command()
    async def dm(self, ctx, user:discord.Member, *, message):
        if user is None:
            await ctx.send("You must specify a user")
        elif message is None:
            await ctx.send("You must enter a message")
        else:
            await user.create_dm()
            await user.dm_channel.send(message)
            #Uncomment this line if bot has perms
            #await ctx.message.channel.purge(limit=1)
    #FIXED by removing the line self.bot.await_process_commands(message)

    #IMPORTANT! USE self.bot to call the bot
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if "gamer" in message.content:
            response = "i hate peple of coler"
            await message.channel.send(response)

            
def setup(bot):
    bot.add_cog(CockAndBallCog(bot))
    print("CockandBall is loaded")
