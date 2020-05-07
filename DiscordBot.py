import discord
import coc

import traceback
from discord.ext import commands

with open("dapi.txt") as f:
    auth = f.readlines()
auth = [x.strip() for x in auth]

clan_tag = auth[4]
coc_client = coc.login(email=auth[2], password=auth[3], key_count=5, key_names ="Bot key", client = coc.EventsClient,)


bot = commands.Bot(command_prefix="!")
CHANNEL_ID = int(auth[1])

@coc_client.event
async def on_clan_member_versus_trophies_change(old_trophies, new_trophies, player):
    await bot.get_channel(CHANNEL_ID).send(
        "{0.name}-nek jelenleg {1} versus trófeája van".format(player, new_trophies))


@bot.command()
async def szia(ctx):
    await ctx.send("Szia!")

@bot.command()
async def hosok(ctx, player_tag):
    player = await coc_client.get_player(player_tag)
    to_send = ""
    for hero in player.heroes:
        to_send += "{}: level {}/{}".format(str(hero), hero.level, hero.max_level)
    await ctx.send(to_send)

@bot.command()
async def parancsok(ctx):
    await ctx.send("!szia, !hosok \{player_tag\}, !tagok")

@bot.command()
async def tagok(ctx):
    members = await coc_client.get_members(clan_tag)

    to_send = "A tagok:\n"
    for player in members:
        to_send += "{0} ({1})\n".format(player.name, player.tag)

    await ctx.send(to_send)

coc_client.add_clan_update(
    [clan_tag], retry_interval=60
)
coc_client.start_updates()


bot.run(auth[0])
