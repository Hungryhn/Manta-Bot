from random import choice, randint
from game_class import Games
import json
import os
from typing import Final
import discord
from discord import Client, Intents, Message, TextChannel
from chatbot import get_chat_response

open_json = open("Game Block.JSON")
game_json = json.load(open_json)
open_json.close()

intents: Intents = discord.Intents.default()
client: Client = Client(command_prefix=';', intents=intents)


async def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()



    # help commands
    if lowered == ';':
        return 'Please enter something!'
    elif ';hello' == lowered:
        return '```python\nHi!\n```'
    elif ';mhelp' == lowered:
        return ('```python\nUse ";" before commands.\nPlease enter ";mhelp commands" for the list of commands.'
                '\nAlso, you can use "?" for sending private responses\n```')
    elif ';mhelp commands' == lowered:
        return ('```python\nCommands are in progress, but here are the completed:\n'
                ';hello ;mhelp ;roll ;coinflip ;location ;binary ;game\n```')


    elif ';location' == lowered:
        location: Final[str] = os.getenv('LOCATION')
        if location == "local":
            return "```python\nBot is running locally!\n```"
        elif location == 'server':
            return "```python\nBot is running on the server!\n```"
        else:
            return f"```python\nError! Output: {location}\n```"
    elif ';binary ' == lowered[0:8]:
        return f"!Your text converted to binary:\n{''.join(format(ord(i), '08b') for i in lowered[8:])}\n```"


    # fun commands
    elif ';roll ' == lowered[0:6]:
        return f'```python\nYou rolled {randint(1, int(lowered[5:]))}\n```'
    elif ';coinflip' == lowered[0:9]:
        return f'```\n{choice(['It is heads.',
                       'It is tails.'])}\n```'
    elif ';praise' == lowered:
        return '\\\python\nManta Bot have been praised!\n```'
    elif ';antigravity' == lowered:
        return '```python\n[Anti Gravity](<https://xkcd.com/353/>)\n```'
    elif ';chat ' == lowered[:6]:
        return f'```python\n{get_chat_response(lowered[6:])}\n```'


    # playlist commands
    elif ';ws 2' == lowered:
        return "```python\n[Here is the playlist's second volume](<https://youtube.com/playlist?list=PLf0ftnImtdgEZ-es2N1k3WxVHDWXBMDPE&si=RTU3xR8YT-OnhMtx>)\n```"
    elif ';ws 1' == lowered:
        return "```python\n[Here is the playlist's first volume](<https://youtube.com/playlist?list=PLf0ftnImtdgEvlJef6bp7xLUVC0BuJByf&si=wmYlIavI5Vv0argt>)\n```"


    # game recommendation commands
    elif ';game ' == lowered[0:6]:
        game_g = lowered[7:]
        if game_g == "action-adventure" or "action adventure":
            return f'```python\nDeveloper\'s pick: {choice(action_adventure_list)}\n```'

        elif game_g == "deckbuilding" or "deck building" or "deck builder":
            return f'```python\nDeveloper\'s pick: {choice([Dicey_dungeons,
                                                 Inscryption])}\n```'

        elif game_g == "management" or "manager" or "manage":
            return f'```python\nDeveloper\'s pick: {choice([Spiritfarer,
                                                 Stacklands])}\n```'


        else:
            return "```python\nSorry, we couldn't find that!\n```"

    elif ";json" == lowered:
        return f'```json\ngame_json["Dicey_d"]\n```'





    else:
        return ''


# Write Stacklands description!

Dicey_d_steam: str = "https://store.steampowered.com/app/861540/Dicey_Dungeons/"
Dicey_dungeons: str = f"[Dicey Dungeons]({Dicey_d_steam}), is an indie deckbuilder game developed by Terry Cavanagh, where you play in a show turned into a dice and your objective is to escape through six chapters with six different characters (and a secret one), so if you like indie deck builder games, this game is probably for you. For more about this game, use the \';about\' command."

Inscryption_steam: str = "https://store.steampowered.com/app/1092790/Inscryption/"
Inscryption: str = f"[Inscryption]({Inscryption_steam}), is an indie deckbuilding themed game where your objective is to escape the game masters. To achieve this you need to explore and improve your deck with various unique cards to achieve victory. If you like horror deckbuilder games, than you will love this game\'s aesthetics. For more about this game, use the \';about\' command."

Jttsp_steam: str = "https://store.steampowered.com/app/973810/Journey_To_The_Savage_Planet/"
Jttsp: str = f"[Journey to the Savage Planet (Jttsp)]({Jttsp_steam}), is an indie action-adventure game developed by Typhoon studios, and published by 505 Studios where you pick up on a mission to explore an alien planet and restore the planets core. For more about this game, use the \';about\' command."

Lethal_c_steam: str = "https://store.steampowered.com/app/1966720/Lethal_Company/"
Lethal_company: str = f"[Lethal Company]({Lethal_c_steam}), is an indie game developed by Zeekerss, where you pick up on a mission to scavenge for scraps and meet quota. It\'s really fun in multiplayer and despite being in early access it blew up in popularity and already has a lot of different fun mods. For more about this game, use the \';about\' command."

Spiritfarer_steam: str = "https://store.steampowered.com/app/972660/Spiritfarer_Farewell_Edition/"
Spiritfarer: str = f"[Spiritfarer]({Spiritfarer_steam}), is an indie management game developed by Thundrelotus Games, where your objective is to pick up as the new spiritfarer to care for your friends to bring them to the afterlife. If you like to just chill and play than this game is just for you. With it\'s cozy environment, this game will pull you in. For more about this game, use the \';about\' command."

Stacklands: str = f"Stacklands..."

action_adventure_list: list = [Jttsp, Lethal_company]
