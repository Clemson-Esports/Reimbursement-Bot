import discord
import requests
from discord.ext import commands
import os
from dataclasses import dataclass

### IMPORTANT VARS ###
request_channel = 1027475253611466752  # Channel that the bot sends messages in.
approved_channel = 1027475279293206560
denied_channel = 1027475297563594762
archived_channel = 1027475393646710814
self_id = 1027441846793801738
message_read_limit = 200
version = '1.0'

######################



valid_commands = ["$request", "$claim", "$status"]
intents = discord.Intents().all()
bot = commands.Bot(command_prefix='^', intents = intents)

# Startup function.
@bot.event
async def on_ready():
    
    print('Bot is online')


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

        # Get the last 200 messages from the request channel.
        request_messages = [message async for message in request.history(limit=message_read_limit)]
        user_requests = []
        for message in request_messages:
            

        # Request prompt.
        if message_array[0].startswith("$request"):
            if len(message_array) >= 3:
                if float(message_array[1]) >= 0:
                    await message.channel.send("Ticket recieved!")
                    sent = await request.send(str(message.author.id) +"\n-------\n" + "USR:\t" + str(message.author) + "\nAMT:\t" + str(message_array[1]) + "\nFOR:\t" + " ".join(message_array[2:]) + "\n-------")
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
    # Don't trigger on self reactions.
    if payload.user_id == self_id:
        return

    # Debug info.
    #print("Message id: " + str(payload.message_id))
    #print("User id: " + str(payload.user_id))
    return










bot.run('MTAyNzQ0MTg0Njc5MzgwMTczOA.GQJRdz.TWoNE0NKjHooJzwXSdMa9bN7qD3JXS1AwFH_e0')