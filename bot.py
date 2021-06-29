# coding: utf-8

# import requests
import discord
import re

# Custom sprite is displayed in the thumbnail
compact_mode = "compact_mode"

# Custom sprite is displayed in the thumbnail, autogen equivalent is displayed
safe_mode = "safe_mode"

# Custom sprite is displayed, autogen equivalent is displayed in the thumbnail
extended_mode = "extended_mode"

display_mode = compact_mode


bot = discord.Client()
bot_id = None
avatar_url = None

autogen_fusion_url = "https://raw.githubusercontent.com/Aegide/FusionSprites/master/Japeal/"

sprite_gallery_id = 858107956326826004
bot_log_id = 616239403957747742
infinite_fusion_discord_id = 293500383769133056

bot_log_channel = None

green_colour = discord.Colour(0x2ecc71)
orange_colour = discord.Colour(0xe67e22)
red_colour = discord.Colour(0xe74c3c)

title_ignored = "Ignored"
title_accepted = "Accepted"

description_missing_sprite = "Missing fusion sprite"
description_missing_fusion_id = "Unable to identify fusion sprite"
description_error = "Please contact Aegide"

def apply_compact_mode(embed, attachment_url, autogen_url):
    if attachment_url:
        embed.set_thumbnail(url=attachment_url)
    return embed

def apply_safe_mode(embed, attachment_url, autogen_url):
    if attachment_url:
        embed.set_thumbnail(url=attachment_url)
    if autogen_url:
        embed.set_image(url=autogen_url)
    return embed

def apply_extended_mode(embed, attachment_url, autogen_url):
    if attachment_url:
        embed.set_image(url=attachment_url)
    if autogen_url:
        embed.set_thumbnail(url=autogen_url)
    return embed

def apply_display_mode(embed, display_mode, attachment_url, autogen_url):
    if display_mode == compact_mode:
        embed = apply_compact_mode(embed, attachment_url, autogen_url)

    elif display_mode == safe_mode:
        embed = apply_safe_mode(embed, attachment_url, autogen_url)

    elif display_mode == extended_mode:
        embed = apply_extended_mode(embed, attachment_url, autogen_url)

    return embed

def create_embed(valid_fusion, description, jump_url):
    if valid_fusion:
        title = title_accepted + " : " + description
        colour = green_colour
    else:
        title = title_ignored + " : " + description
        colour = orange_colour

    return discord.Embed(title=title, colour=colour, description="[Link to message](" + jump_url + ")")
        
def extract_data(message):
    valid_fusion = False
    description = description_error
    attachment_url = None
    autogen_url = None

    if len(message.attachments) >= 1:
        filename = message.attachments[0].filename
        attachment_url = message.attachments[0].url
        pattern = '([0-9]+)\.([0-9]+)'
        result = re.match(pattern, filename)
        if result:
            # Existing attachment + valid file name
            valid_fusion = True
            fusion_id = result[0]
            description = fusion_id
            autogen_url = autogen_fusion_url + fusion_id.split(".")[0] + "/" + fusion_id + ".png"

        else:
            result = re.match(pattern, message.content) 
            if result:
                # Existing attachment + valid description
                valid_fusion = True
                fusion_id = result[0]
                description = fusion_id
                autogen_url = autogen_fusion_url + fusion_id.split(".")[0] + "/" + fusion_id + ".png"

            else:
                # Existing attachment + impossible to detect fusion id
                description = description_missing_fusion_id
    
    else:
        # Missing attachment (no sprite)
        description = description_missing_sprite

    return valid_fusion, description, attachment_url, autogen_url


@bot.event
async def on_ready():

    global bot_id
    app_info = await bot.application_info()
    bot_id = app_info.id
    permission_id = "2048"

    global avatar_url
    owner = app_info.owner
    avatar_url = owner.avatar_url_as(static_format='png', size=256)

    global bot_log_channel
    infinite_fusion_discord_server = bot.get_guild(infinite_fusion_discord_id)
    bot_log_channel = infinite_fusion_discord_server.get_channel(bot_log_id)

    print("\n\n")
    print("Ready! bot invite:\n\nhttps://discordapp.com/api/oauth2/authorize?client_id=" + str(bot_id) + "&permissions=" + permission_id + "&scope=bot")
    print("\n\n")

@bot.event
async def on_guild_join(guild):
    print("JOINED THE SERVER :", guild)

@bot.event
async def on_guild_remove(guild):
    print("REMOVED FROM THE SERVER :", guild)

@bot.event
async def on_message(message):
    if(message.channel.id == sprite_gallery_id):

        valid_fusion, description, attachment_url, autogen_url = extract_data(message)

        embed = create_embed(valid_fusion, description, message.jump_url)
        embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
        embed.set_footer(text=message.content)
        embed = apply_display_mode(embed, display_mode, attachment_url, autogen_url)

        await bot_log_channel.send(embed=embed)
    pass


def get_fusion_id(content):
    print(content.split("."))

"""
@bot.event
async def on_command_error(ctx, error):
    print(ctx.author, ":", ctx.message.content, ":", error)

@bot.command()
async def f(ctx):
    content = ctx.message.content[3:]
    split = content.split(" ")
    poke_head = split[0]
    poke_body = split[1]
    fusion = poke_head + "." + poke_body
    filename = poke_head + "." + poke_body + ".png"
    url = fusion_url + filename

    username = ctx.message.author
    server = ctx.message.guild

    if(requests.get(url).status_code == 200):
        embed = discord.Embed(title=fusion, description="Custom sprite")
        embed.set_footer(text="Aegide", icon_url=avatar_url)
        embed.set_image(url=url)
        print(username, ":", fusion, "(", server, ")")
        await ctx.channel.send(embed=embed)
    else:
        url = japeal_url + poke_head + "/" + filename

        if(requests.get(url).status_code == 200):
            embed = discord.Embed(title=fusion, description="Autogen sprite")
            embed.set_footer(text="Aegide", icon_url=avatar_url)
            embed.set_image(url=url)
            print(username, ":", fusion, "(", server, ")")
            await ctx.channel.send(embed=embed)
        else:
            print(username, ":", fusion, ":", "NOT FOUND", "(", server, ")")
            await ctx.channel.send(content=message_not_found)
"""

# The token of the bot is stored inside a file
token = open("token.txt").read().rstrip()
bot.run(token)