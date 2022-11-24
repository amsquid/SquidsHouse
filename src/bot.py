# Imports
import discord

from discord.ext import commands
from room import Room

# Get data from config.dat
config = {}

with open('./config.dat', 'r') as configFile:
	data = configFile.read()

	lines = data.split(' ')

	for line in lines:
		config_item = line.split('=')

		key = str(config_item[0])
		value = str(config_item[1].replace('\n', ''))
		
		config[key] = value

# Variables
token = config['token']

rooms = []

# Setup discord bot
bot: commands.bot.Bot = commands.bot.Bot(command_prefix="!", intents=discord.Intents.all())

# Functions
def create_room(name, permission):
	newRoom = Room(name, permission)

	rooms.append(newRoom)

# Commands
@bot.command(name='rooms')
async def _rooms(ctx: commands.Context):
	roomsOut = ''

	for room in rooms:
		roomsOut += str(room.roomName) + '\n'

	await ctx.reply('The following rooms are avaliable```\n' + roomsOut + '```')

# Setting up rooms
create_room('LivingRoom', 1041057800090038393)
create_room('Kitchen', 1041057809225240686)
create_room('Bedroom', 1041057809946652792)

# Events
@bot.event
async def on_ready():
	print(bot.user.name, 'is ready!')

# Bot login
bot.run(token)