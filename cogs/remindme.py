import types
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
import typing
import datetime
import pymongo
from dotenv import load_dotenv
import os

#Loading database
DATABASE = os.getenv("DATABASE_CONNECTION")
client = pymongo.MongoClient(DATABASE)
db = client["Reminders"]
collection = db["ReminderList"]


types = [
        "min",
        "minutes",
        "mins",
        "minute",
        "hour",
        "hr",
        "hours",
        "hrs",
        "days",
        "day",
    ]

class reminders(commands.Cog, name="reminders"):
    
    def __init__(self, bot):
        self.bot = bot
        self.check_reminders.start()

    @commands.command()
    async def db_check(self, ctx):
        print(f"test")
        print(client.list_database_names())

    @commands.command(name="remindme", aliases=["rm"])
    async def remindme(self,ctx, user: commands.Greedy[discord.Member], TimeValue, DateType, *, Reminder):

        if(DateType in types):
            #convert everything to minutes
            if DateType.startswith("m"):
                time = int(TimeValue)
            elif DateType.startswith("h"):
                time = int(TimeValue) * 60
            elif DateType.startswith("d"):
                time = int(TimeValue) * 1440
            
            #Figure out date in which to send reminder

            current_date = datetime.datetime.now()
            hours_added = datetime.timedelta(minutes= time)
            remind_date = current_date + hours_added
    
            #create reminder value
            reminder = {
                'user': ctx.author,
                'date': remind_date,
                'message': Reminder
            }

            print(f"Successfully uploaded reminder to DB by user {ctx.message.author}, id: {ctx.message.author.id}.")

            #Add reminder to DB
            collection.insert_one(reminder)

        else:
            await ctx.send("Please enter a valid unit of time! (Minute, Hour, Day)")

    @tasks.loop(minutes=1)
    async def check_reminders(self):
        current_date = datetime.datetime.now()
        myquery = {'date': {'$lt': current_date}}

        print('Checking Reminders...')
        for x in collection.find(myquery):
            userId = int(x['user'])
            user = self.bot.get_user(userId)
            message = x['message'] 
            embed=discord.Embed(title="Sample Embed", 
            description=message, color=discord.Color.purple())  
            user.send(embed=embed)   
        

            
          
    @remindme.error
    async def remindme_error(self, ctx, error: commands.CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            message = f"You're missing part of the command! Try again, and add a {error.param}"
        else:
            message = "Uh oh! Something went wrong. Try again!"
            print(error)

        await ctx.send(message, delete_after=5)
        await ctx.message.delete(delay=5)

    
        

def setup(bot):
    bot.add_cog(reminders(bot))