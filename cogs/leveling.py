import discord
from discord.ext import commands
import asyncio 
import datetime
import pymysql
import os
import math
from dotenv import load_dotenv

load_dotenv(r"C:\Users\justi\Discord V1.0\keys.env")
host = os.getenv("host")
port = int(os.getenv("port"))
dbname = os.getenv("dbname")
username = os.getenv("username")
password = os.getenv("password")


class LevelingCog(commands.Cog, name = "Leveling"):
    def __init__(self, bot):
        self.bot = bot 

    #Fixed
    @commands.Cog.listener()
    async def on_message(self, message):
        #Prevents the bot from being logged in the database
        if message.author == self.bot.user:
            return
        db = pymysql.connect(host, user=username, password=password, db=dbname)
        cursor = db.cursor()
        #grab id of message author
        sql = ("SELECT `user_id` FROM `levels` WHERE `guild_id` = %s and `user_id` = %s")
        val = ({message.author.guild.id}, {message.author.id})
        cursor.execute(sql, val)
        result = cursor.fetchone()
        #if not in db, add them 
        #FIXED BY changing "message" to "message.author.id on line 24......... "
        if result is None:
            sql = ("INSERT INTO `levels` (`guild_id`, `user_id`, `exp`, `lvl`) VALUES(%s, %s, %s, %s)")
            val = (message.author.guild.id, message.author.id, 2, 0)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
        else:              #user_id is index 0, exp is index 1, etc...
            sql = ("SELECT `user_id`, `exp`, `lvl` FROM `levels` WHERE `guild_id` = %s and `user_id` = %s")
            val = ({message.author.guild.id}, {message.author.id})
            cursor.execute(sql, val)
            result1 = cursor.fetchone()
            exp = int(result1[1])
            sql = ("UPDATE levels SET `exp` = %s WHERE `guild_id` = %s and `user_id` = %s")
            val = (exp + 2, str(message.guild.id), str(message.author.id))
            cursor.execute(sql, val)
            db.commit()
            #fetch updated results
            sql = ("SELECT `user_id`, `exp`, `lvl` FROM `levels` WHERE `guild_id` = %s and `user_id` = %s")
            val = ({message.author.guild.id}, {message.author.id})
            cursor.execute(sql, val)
            result2 = cursor.fetchone()
            #fetch initial xp and level
            xp_start = int(result2[1])
            lvl_start = int(result2[2])
            xp_end = math.floor(5 * (lvl_start ** (1/6) + 25 * lvl_start + 10))
            if xp_start > xp_end: 
                await message.channel.send(f"{message.author.mention} has leveled up to level {lvl_start + 1}")
                sql = ("UPDATE `levels` SET `lvl` = %s, `exp` = %s WHERE `guild_id` = %s and `user_id` = %s")
                val = (lvl_start + 1, 0, str(message.guild.id), str(message.author.id))
                cursor.execute(sql, val)
                db.commit()
            cursor.close()
            db.close()

    @commands.command()
    async def rank(self, ctx, person:discord.User=None):
        if person is None:
            db = pymysql.connect(host, user=username, password=password, db=dbname)
            cursor = db.cursor()
            sql = ("SELECT `user_id`, `exp`, `lvl` FROM `levels` WHERE `guild_id` = %s and `user_id` = %s")
            val = (ctx.message.author.guild.id, ctx.message.author.id)
            cursor.execute(sql, val)
            result = cursor.fetchone()
            cursor.close()
            db.close()
            if result is None:
                await ctx.send("That user is not yet ranked")
            else:
                await ctx.send(f"{ctx.message.author.name} is currently level '{str(result[2])}' and has '{str(result[1])}' XP")
        else:
            db = pymysql.connect(host, user=username, password=password, db=dbname)
            cursor = db.cursor()
            sql = ("SELECT `user_id`, `exp`, `lvl` FROM `levels` WHERE `guild_id` = %s and `user_id` = %s")
            val = (ctx.message.author.guild.id, person.id)
            cursor.execute(sql, val)
            result = cursor.fetchone()
            cursor.close()
            db.close()
            if result is None:
                await ctx.send("That user is not yet ranked")
            else:
                await ctx.send(f"{person.name} is currently level '{str(result[2])}' and has '{str(result[1])}' XP")
            
        
        
def setup(bot):
    bot.add_cog(LevelingCog(bot))
    print("Leveling is loaded")
