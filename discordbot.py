import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import asyncio
import sys
import datetime
import pymysql

#YOUR .env FILEPATH HERE
#Make sure to get rid of the dotenv stuff when you ssh to the host server
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
host = os.getenv("host")
port = int(os.getenv("port"))
dbname = os.getenv("dbname")
username = os.getenv("username")
password = os.getenv("password")
bot = commands.Bot(command_prefix = '.')


@bot.event
async def on_ready():
    #Select the guild the bot is connected to
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    print(f"{bot.user} has connected to Discord!")
    print(f"{guild.name}(id: {guild.id})")
    members = "\n - ".join([member.name for member in guild.members])
    print(f"Guild members:\n - {members}")

#Loads all of the cogs
initial_extensions = ["cogs.moderation", "cogs.cockandball", "cogs.matrixcalculation", "cogs.leveling", "cogs.messagesearch"]
if __name__ == "__main__":
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f"Failed to load extension {extension}", file=sys.stderr)

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f"Hi {member.name}, welcome to the server")

@bot.event
async def on_error(event, *args, **kwargs):
    with open("err.log", "a") as f:
        if event == "on_message":
            f.write(f"Unhandled message: {args[0]}\n")
try:
    bot.run(TOKEN)
except:
    print("Error running bot")
finally:
    #IMPORTANT!!!! YOU MUST USE CTRL+C TO CLOSE IT AND NOT KILL TERMINAL!
    #log the last online time for the bot
    #Use DateTime API
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    #get time in UTC
    endTime = datetime.datetime.utcnow()
    db = pymysql.connect(host, user=username, password=password, db=dbname)
    cursor = db.cursor()
    sql = ("SELECT `lastonline` FROM `lastonline` WHERE `server_id` = %s")
    val = ({guild.id}, )
    cursor.execute(sql, val)
    result = cursor.fetchone()
    if result is None:
        sql = ("INSERT INTO `lastonline` (`lastonline`, `server_id`) VALUES(%s, %s)")
        val = (endTime, guild.id)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
    else:
        sql = ("UPDATE `lastonline` SET `lastonline` = %s where `server_id` = %s")
        val = (endTime, guild.id)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
    
