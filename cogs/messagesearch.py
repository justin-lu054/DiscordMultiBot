import discord
from discord.ext import commands
import asyncio 
import datetime
import pymysql
from dotenv import load_dotenv
import os
import re

load_dotenv(r"C:\Users\justi\Discord V1.0\keys.env")
GUILD = os.getenv("DISCORD_GUILD")
host = os.getenv("host")
port = int(os.getenv("port"))
dbname = os.getenv("dbname")
username = os.getenv("username")
password = os.getenv("password")

def getContent(message): 
    return message.content 

class MessageSearchCog(commands.Cog, name = "MessageSearch"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            if guild.name == GUILD:
                break
        #Logs all the messages sent since the bot was last online
        db = pymysql.connect(host, user=username, password=password, db=dbname)
        cursor = db.cursor()
        cursor.execute(f"SELECT `time` FROM `lastonline` WHERE `server_id` = `{guild.id}`")
        result = cursor.fetchone()
        stringDate = result[0]
        #Converts the string stored in db back to datetime.datetime object 
        lastOnline = datetime.datetime.strptime(stringDate, '%Y-%m-%d %H:%M:%S.%f')
        #YOUR CHANNEL ID HERE 
        channel = guild.get_channel(YOUR_CHANNEL_ID_HERE)
        if result is None:
            async for message in channel.history(limit=None):
                sql = ("INSERT INTO `messagelog` (`user_id`, `server_id`, `messagetext`) VALUES(%s, %s, %s)")
                val = (message.author.id, message.author.guild.id, message.content)
                cursor.execute(sql, val)
        else:
            async for message in channel.history(after=lastOnline):
                sql = ("INSERT INTO `messagelog` (`user_id`, `server_id`, `messagetext`) VALUES(%s, %s, %s)")
                val = (message.author.id, message.author.guild.id, message.content)
                cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

    @commands.group(invoke_without_command=True)
    async def search(self, ctx):
        commands = "Avaliable Commands:\nphone <user>\nemail <user>\nregex <regex> <user>"
        await ctx.send(commands)

    #Done
    #FIGURE OUT HOW TO USE REGEXP WITH MYSQL3
    @search.command()
    async def phone(self, ctx, person:discord.Member):
        if person is None:
            await ctx.send("You must specify a member of this server")
        else:
            db = pymysql.connect(host, user=username, password=password, db=dbname)
            cursor = db.cursor()
            #Consider pulling all messages and using python regex
            phoneRegex = re.compile(r"((\d{3}|\(\d{3}\))?(\s|-|\.)?(\d{3})(\s|-|\.)(\d{4})(\s*(ext|x|ext.)\s*(\d{2,5}))?)", re.VERBOSE)
            #This regex not working 
            sql = ("SELECT DISTINCT `messagetext` FROM `messagelog` WHERE `user_id` = %s and `server_id` = %s")
            val = (person.id, ctx.message.guild.id)
            cursor.execute(sql, val)
            messages = cursor.fetchall()
            output = "Phone numbers found:\n"
            for x in messages:
                foundNumbers = phoneRegex.findall(x[0])
                for numbers in foundNumbers: 
                    output += numbers[0]
                    output += "\n"
            await ctx.send(output)
            db.commit()
            cursor.close()
            db.close()
    
    #Done 
    @search.command()
    async def email(self, ctx, person:discord.Member):
        if person is None:
            await ctx.send("You must specify a member of this server")
        else:
            emailRegex = re.compile(r"""(
                            [a-zA-Z0-9._%+-]+
                            @
                            [a-zA-Z0-9.-]+
                            (\.[a-zA-Z]{2,10})
                            )""", re.VERBOSE)
            db = pymysql.connect(host, user=username, password=password, db=dbname)
            cursor = db.cursor()
            regex = r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+(\.[a-zA-Z]{2,10}))"
            sql = ("SELECT DISTINCT `messagetext` FROM `messagelog` WHERE `user_id` = %s and `server_id` = %s and `messagetext` REGEXP %s")
            val = (person.id, ctx.message.guild.id, regex)
            cursor.execute(sql, val)
            messages = cursor.fetchall()
            output = "Emails found:\n"
            for x in messages:
                #Extract ONLY the email found
                foundEmails = emailRegex.findall(x[0])
                for emails in foundEmails:
                    output += emails[0]
                    output += "\n"

            await ctx.send(output)
            db.commit()
            cursor.close()
            db.close()

    @commands.Cog.listener()
    async def on_message(self, message):
        #Ignores any message sent by the bot
        if message.author == self.bot.user:
            return
        #Logs all messages sent to the server
        db = pymysql.connect(host, user=username, password=password, db=dbname)
        cursor = db.cursor()
        sql = ("INSERT INTO `messagelog` (`user_id`, `server_id`, `messagetext`) VALUES(%s, %s, %s)")
        val = (message.author.id, message.author.guild.id, message.content)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

def setup(bot):
    bot.add_cog(MessageSearchCog(bot))
    print("MessageSearch is loaded")
