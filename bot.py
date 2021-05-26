import discord
import platform
import os
import sys
import yaml
import random
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord.ext.commands import Bot
import pymongo

#load config
if not os.path.isfile("config.yaml"):
    sys.exit("config.yaml not found! Please try again.")
else:
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

#Declare bot
bot = Bot(command_prefix=config["bot_prefix"])


#get token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# On Ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    status_task.start()

#Set Game Status
@tasks.loop(minutes=1.0)
async def status_task():
    statuses = ["!remindme, !rm", "with reminders!", "with code..."]
    await bot.change_presence(activity=discord.Game(random.choice(statuses)))

#load cogs
if __name__ == "__main__":
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"cogs.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")


#Runs on every command
@bot.event
async def on_command_completion(ctx):
    fullCommandName = ctx.command.qualified_name
    split = fullCommandName.split(" ")
    executedCommand = str(split[0])
    print(
        f"Executed {executedCommand} command in {ctx.guild.name} (ID: {ctx.message.guild.id}) by {ctx.message.author} (ID: {ctx.message.author.id})")

    
bot.run(TOKEN)