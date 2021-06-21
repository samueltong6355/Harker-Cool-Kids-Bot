import discord
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix = ".")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.listen("on_message")
async def on_message(message):
    splited_message = message.content.split()
    guilds = []
    for guild in client.guilds:
        guilds.append(guild.id)

    if message.author == client.user:
        return

    print(modmail_id)

    if message.guild == None:
        try:
            guild_id = int(splited_message[0], base=10)
            if guild_id in guilds:
                found_modmail = False
                for category in client.get_guild(guild_id).categories:
                    if category.name == "Modmail":
                        found_modmail = True
                        break

                if found_modmail:
                    channel_name = "{}s-mail".format(str(message.author).lower().replace("#", ""))
                    found_channel = False

                    for c in client.get_guild(guild_id).channels:
                        if c.name == channel_name:
                            found_channel = True
                            break

                    if found_channel:
                        await message.author.send("You already have a mail channel created! Your message is being sent.")
                    else:
                        await message.author.send("We are going to create a channel for your mail then send your message.")
                        await client.get_guild(guild_id).create_text_channel(channel_name, category = discord.utils.get(client.get_guild(guild_id).categories, name = "Modmail"))

                    mail = splited_message[1:]
                    await discord.utils.get(client.get_guild(guild_id).channels, name = channel_name).send(" ".join(mail))

                else:
                    await message.author.send("The guild is was valid however, there is no category for your mail yet. Please contact someone with administrative permissions to fix this.")
        except:
            pass


@client.command()
async def setup(ctx):
    if (discord.utils.get(ctx.message.guild.categories, name = "Modmail") == None):
        await ctx.message.guild.create_category("Modmail")
    else:
        await ctx.send("No need for setup! Modmail category already created!")

client.run("ODU1NjMwNjkyNzc0NzA3MjUy.YM1SLg.82FrE0HKEdODK3NMBwjPvO9MWos")