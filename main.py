import discord
import requests
from discord.ext import commands
import os
from dataclasses import dataclass

### IMPORTANT VARS ###
reimbursement_channel = 1027446080369086535  # Channel that the bot creates threads in.
version = '1.0'

######################
#intents = discord.Intents.all()
#client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='^')
send_channel = bot.get_channel(reimbursement_channel)


@bot.event
async def on_ready():
    print('Bot is online')

@bot.event
async def on_message(message):
    
    print("message: " + str(len(message.content)))

    if message == bot.user:
        await message.channel.send('self message')
        return

    if type(message.channel) == discord.channel.DMChannel:
        print("\n\n\nMESSAGE\n\n\n")
        await send_channel.send("hello")
        return

    if message.content == 'reimbursement.version':
        print("\n\n\nMESSAGE\n\n\n")
        await message.channel.send(f'My version number is: {version}')



bot.run('MTAyNzQ0MTg0Njc5MzgwMTczOA.GQJRdz.TWoNE0NKjHooJzwXSdMa9bN7qD3JXS1AwFH_e0')