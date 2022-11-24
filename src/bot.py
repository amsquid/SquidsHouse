# Imports
import discord

from discord import app_commands
from discord.ext import commands

import Room from "./room"

# Get data from config.dat
config = {}

with open('./config.dat', 'r') as configFile:
    data = configFile.read()

    lines = data.split(' ')

    for line in lines:
        config_item = line.split('=')

        key = str(config_item[0])
        value = str(config_item[1].replace('\n', ''))

        print(key + "=" + value)
        
        config[key] = value

# Variables
token = config['token']

# Setup discord bot
bot = commands.bot(command_prefix="!", intents = discord.Intents.all())

# Commands
@bot.command()
def help(ctx: discord):
    ctx.

# Events

# Bot login
