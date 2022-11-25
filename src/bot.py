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
notifications_channel = 1041056231986569306

default_room = None

# Setup discord bot
client = discord.Client(intents=discord.Intents.all())
tree = discord.app_commands.tree.CommandTree(client)

# Functions
def create_room(name, permission, default=False):
	global default_room

	newRoom = Room(name, permission)
	rooms.append(newRoom)

	if default:
		default_room = newRoom

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
	member = interaction.user

	room = room.lower()

	gotoRoom = None

	# Getting room the user inputted and logging all the roles
	for roomClass in rooms:
		if roomClass.roomName == room:
			gotoRoom = roomClass

		roleId = roomClass.requiredPermission
		roles.append(discord.utils.get(member.guild.roles, id=roleId))

	# Getting group needed for room
	roomPermission = gotoRoom.requiredPermission
	roomRole = discord.utils.get(member.guild.roles, id=roomPermission)

	# Clearing room permissions
	for role in roles:
		await member.remove_roles(role)

	# Adding the main room's permissions
	await member.add_roles(roomRole)

	# Sending response
	await interaction.response.send_message(member.display_name + ' has left the room')

@tree.command(guild=discord.Object(id=main_guild), name='notification', description="Sends a notification to all user's phones")
async def _notification(interaction: discord.Interaction, message: str):
	member = interaction.user

	if member.guild_permissions.administrator:
		await client.get_channel(notifications_channel).send('**NEW NOTIFICATION**\n' + message)

		await interaction.response.send_message('Sent message!')
	else:
		await interaction.response.send_message('You cannot send notifications')

# Setting up rooms
create_room('livingroom', 1041057800090038393, True)
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

@client.event
async def on_member_join(member: discord.Member):
	# Getting needed permission
	permission = default_room.requiredPermission

	# Adding user to that permission
	role = discord.utils.get(member.guild.roles, id=permission)

	await member.add_roles(role)

# Bot login
client.run(token)