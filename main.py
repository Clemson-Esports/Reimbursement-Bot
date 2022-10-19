import discord
import requests
from discord.ext import commands
import os
from dataclasses import dataclass

### IMPORTANT VARS ###
#request_channel = 1027475253611466752  # Channel that the bot sends messages in.
#approved_channel = 1027475279293206560
#denied_channel = 1027475297563594762
#archived_channel = 1027475393646710814

request_channel = 1032135191558373446  # Channel that the bot sends messages in.
approved_channel = 1032135238891085854
denied_channel = 1032135266074378250
archived_channel = 1032135328590462986

channels = [request_channel, approved_channel, denied_channel, archived_channel]
self_id = 1027441846793801738
message_read_limit = 200
version = '1.0'

######################



valid_commands = ["$request", "$claim", "$status", "$confirm"]
intents = discord.Intents().all()
bot = commands.Bot(command_prefix='^', intents = intents)

# Startup function.
@bot.event
async def on_ready():
    print('Bot is online')



# Need to make a function to send messages in a given format to improve readability.

# Need error checking function also.

# Need a function to move messages between channels. 

# Need a function to send DMs back to users.

async def move_message(current_channel, move_channel, message_payload):
    msgID = message_payload.message_id
    msg = await current_channel.fetch_message(msgID)
    msgStr = msg.content
    sent = await move_channel.send(msgStr)
    await sent.add_reaction('✅')
    await sent.add_reaction('⛔')
    await msg.delete()

async def dm_user(user_id, send_msg):
    usr = bot.get_user(user_id)
    channel = await usr.create_dm()
    await channel.send(send_msg)

# On message event.
@bot.event
async def on_message(message):

    # No interaction with other bots.
    if message.author.bot:
        return

    if message == bot.user:
        await message.channel.send('self message')
        return

    # If message is from DM.
    if type(message.channel) == discord.channel.DMChannel:
        # Message should be formatted $command [$ amount] [desc]
        message_array = message.content.split()
        # Get channels
        request = bot.get_channel(request_channel)
        approved = bot.get_channel(approved_channel)
        denied = bot.get_channel(denied_channel)
        archived = bot.get_channel(archived_channel)

        # Get the last 200 messages from the 4 channels.
        request_messages = [message async for message in request.history(limit=message_read_limit)]
        approved_messages = [message async for message in approved.history(limit=message_read_limit)]
        denied_messages = [message async for message in denied.history(limit=message_read_limit)]
        archived_messages = [message async for message in archived.history(limit=message_read_limit)]
        # Find all requests from user and store in an array.
        user_requests = []
        user_approved = []
        user_denied = []
        user_archived = []

        for msg in request_messages:
            if msg.author == self_id and int(msg.content.partition('\n')[0]) == message.author.id:
                user_requests.append(msg.content)

        for msg in approved_messages:
            if msg.author == self_id and int(msg.content.partition('\n')[0]) == message.author.id:
                user_approved.append(msg.content)

        for msg in denied_messages:
            if msg.author == self_id and int(msg.content.partition('\n')[0]) == message.author.id:
                user_denied.append(msg.content)

        for msg in archived_messages:
            if msg.author == self_id and int(msg.content.partition('\n')[0]) == message.author.id:
                user_archived.append(msg.content)

        user_msg_count = len(user_requests) + len(user_approved) +len(user_denied) +len(user_archived)

        # Request prompt.
        if message_array[0].startswith("$request"):
            if len(message_array) >= 3:
                if float(message_array[1]) >= 0:
                    print("Ticket Recieved!")
                    await message.channel.send("Ticket recieved!")
                    sent = await request.send(str(message.author.id) +"\n-------\n" + "USR:    " + str(message.author) + "\nAMT:    " + str(message_array[1]) + "\nFOR:    " + " ".join(message_array[2:]) + "\n-------")
                    await sent.add_reaction('✅')
                    await sent.add_reaction('⛔')
        
        elif message_array[0].startswith("$claim"):
            await message.channel.send("claim")

        elif message_array[0].startswith("$status"):
            await message.channel.send("status")

        else:
            await message.channel.send("Invalid command!")

        return

    if message.content == 'reimbursement.version':
        await message.channel.send(f'My version number is: {version}')


# When a reaction is added this function is called.
@bot.event
async def on_raw_reaction_add(payload):

    # Get channels
    request = bot.get_channel(request_channel)
    approved = bot.get_channel(approved_channel)
    denied = bot.get_channel(denied_channel)
    archived = bot.get_channel(archived_channel)

    # Don't trigger on self reactions.
    if payload.user_id == self_id:
        return

    # Don't trigger on emojis not in given channels.
    if payload.channel_id not in channels:
        return

    message_id = payload.message_id
    message_channel = bot.get_channel(payload.channel_id)
    message_content = await message_channel.fetch_message(message_id)
    message_content = message_content.content
    message_split = message_content.splitlines()
    user_id = int(message_split[0])
    user_name = message_split[2][8:]
    amount = int(message_split[3][8:])
    description = message_split[4][8:]


    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
    # DM_USER NEEDS TO BE CALLED BEFORE MOVE_MESSAGE!!! #
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #

    # Request Channel -> Approved
    if payload.channel_id == request_channel and str(payload.emoji) == '✅':
        await dm_user(user_id, "Your request for $" + str(amount) + " for " + description + " has been approved.")
        await move_message(request, approved, payload)
    # Request Channel -> Denied
    if payload.channel_id == request_channel and str(payload.emoji) == '⛔':
        await dm_user(user_id, "Your request for $" + str(amount) + " for " + description + " has been denied.")
        await move_message(request, denied, payload)
    # Approved Channel -> Archived
    if payload.channel_id == approved_channel and str(payload.emoji) == '✅':
        await move_message(approved, archived, payload)
    # Approved Channel -> Requests
    if payload.channel_id == approved_channel and str(payload.emoji) == '⛔':
        await move_message(approved, request, payload)
    # Denied Channel -> Requests
    if payload.channel_id == denied_channel and str(payload.emoji) == '✅':
        await move_message(denied, request, payload)

    # Debug info.
    #print("Message id: " + str(payload.message_id))
    #print("User id: " + str(payload.user_id))
    return










bot.run('MTAyNzQ0MTg0Njc5MzgwMTczOA.GQJRdz.TWoNE0NKjHooJzwXSdMa9bN7qD3JXS1AwFH_e0')