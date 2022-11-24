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

main_guild = 1041055949571498036

# Setup discord bot
client = discord.Client(intents=discord.Intents.all())
tree = discord.app_commands.tree.CommandTree(client)

# Functions
def create_room(name, permission):
	newRoom = Room(name, permission)

	rooms.append(newRoom)

# Commands
@tree.command(guild=discord.Object(id=main_guild), name='rooms', description='Sends all the rooms')
async def _rooms(interaction: discord.Interaction):
	roomsOut = ''

	for room in rooms:
		roomsOut += str(room.roomName) + '\n'

	await interaction.response.send_message('The following rooms are available```\n' + roomsOut + '```')

@tree.command(guild=discord.Object(id=main_guild), name='gotoroom', description='Sends user to a different room')
async def _gotoroom(interaction: discord.Interaction, room: str):	
	roles = []
	author = interaction.user

	room = room.lower()

	gotoRoom = None

	# Getting room the user inputted and logging all the roles
	for roomClass in rooms:
		if roomClass.roomName == room:
			gotoRoom = roomClass

		roleId = roomClass.requiredPermission
		roles.append(discord.utils.get(author.guild.roles, id=roleId))

	# Getting group needed for room
	roomPermission = gotoRoom.requiredPermission
	roomRole = discord.utils.get(author.guild.roles, id=roomPermission)

	# Clearing room permissions
	for role in roles:
		await author.remove_roles(role)

	# Adding the main room's permissions
	await author.add_roles(roomRole)

	# Sending response
	await interaction.response.send_message('Successfully went to room, ' + gotoRoom.roomName)


# Setting up rooms
create_room('livingroom', 1041057800090038393)
create_room('kitchen',    1041057809225240686)
create_room('bedroom',    1041057809946652792)

# Events
@client.event
async def on_ready():
	print('Waiting until the client is ready')
	await client.wait_until_ready()

	print('Syncing commands')
	await tree.sync(guild=discord.Object(id=main_guild))

	print(client.user.name, 'is ready!')

# Bot login
client.run(token)