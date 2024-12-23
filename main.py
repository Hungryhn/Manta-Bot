import datetime
from typing import Final
import os
import requests
import json

import discord

from discord.ext import commands
from dotenv import load_dotenv
from discord import Intents, Client, Message, app_commands
from discord.ext import commands
from responses import get_response
from blacklist import blacklist, time_list, kick_list, red_list


class Mclient(discord.Client):
    def __init__(self, *, intents_: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=1263968856720806001)
        await self.tree.sync(guild=1263968856720806001)


# load token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

intents: Intents = discord.Intents.default()
intents.message_content = True  # NOQA
client: Client = Client(intents=intents)


# function
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('Message was empty.')
        return

    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    try:
        response: str = await get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
        print(response)
    except Exception as e:
        print(e)


# handling messages
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)
    message_binary = ''.join(format(ord(i), '08b') for i in user_message)

    print(f'[{channel}] {username}: "{user_message}"')
    if message.content[:8] == '00111011':
        await send_message(message, message_binary)
    else:
        await send_message(message, user_message)

    if message.content == ';send def':
        def_channel = client.get_channel(1312808698372161687)
        def_message: Message = await def_channel.fetch_message(1312808988894826547)
        _def: str = def_message.content
        var_message: Message = await def_channel.fetch_message(1312809067261198438)
        _var: str = var_message.content
        try:
            await message.channel.send(eval(_def))
        except Exception as send_ex:
            await message.channel.send(send_ex)
    if message.content == ';run def':
        def_channel = client.get_channel(1312808698372161687)
        def_message: Message = await def_channel.fetch_message(1312808988894826547)
        _def: str = def_message.content
        var_message: Message = await def_channel.fetch_message(1312809067261198438)
        _var: str = var_message.content
        try:
            eval(_def)
        except Exception as run_ex:
            await message.channel.send(run_ex)


    if any(kick in message_binary for kick in kick_list):
        await message.delete()
        return

    elif any(worse in user_message for worse in time_list):
        await message.delete()
        await message.author.timeout(datetime.timedelta(minutes=2))
        print(f'{message.author} has been timed out!')
        return

    elif any(black in user_message for black in blacklist):
        await message.delete()
        return

    elif any(red in user_message for red in red_list):
        await client.get_channel(1303422817144143913).send("Red notice: \n```" + message.content + "```\n" + str(message.id)
                                                           + "\nChannel " + message.channel.name + ": " + str(message.channel.id)
                                                           + "\nFrom " + message.author.name + ": " + str(message.author.id) + '\n Payload:\n-# ' + str(message))


    if 'discord.gg/' in user_message:
        if message.author.get_role(1303413958899793941):
            return
        else:
            await message.delete()


@client.event
async def on_raw_message_edit(payload):
    guild = client.get_guild(payload.guild_id)
    channel = client.get_channel(payload.channel_id)
    message: Message = await channel.fetch_message(payload.message_id)
    author = message.author


    message_binary = ''.join(format(ord(i), '08b') for i in payload.data['content'])
    if any(kick in message_binary for kick in kick_list):
        await message.delete()
        return

    elif any(timeout in payload.data['content'] for timeout in time_list):
        await message.delete()
        await payload.data['user'].timeout(datetime.timedelta(minutes=2))
        print(f'{payload.data['user']} has been timed out!')
        return

    elif any(black in payload.data['content'] for black in blacklist):
        await message.delete()
        return

    elif any(red in payload.data['content'] for red in red_list):
        await client.get_channel(1303413958899793941).send("Red notice: \n```" + payload.data['content'] + "```\n" + str(payload.message_id)
                                                           + "\nChannel " + channel.name + ": " + str(channel.id)
                                                           + "\nFrom " + str(author.id) + ": " + author.name + '\n Payload:\n-# ' + str(payload))


    if 'discord.gg/' in payload.data['content']:
        if author.get_role(1303413958899793941):
            return
        else:
            await message.delete()


@client.event
async def on_message_delete(message):
    if ';test delete' in message.content:
        await client.get_channel(1303422817144143913).send(message.content)


@client.event
async def on_ready():
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name='Manta Bot | use ";mhelp"'))

    print(f'{client.user} is now running')


@commands.command()
async def mhelp(interaction: discord.Interaction):
    await interaction.channel.send("```[Insert Text Here]```")


# main entry
def main() -> None:
    client.run(token=TOKEN)


if __name__ == '__main__':
    main()

#