import discord
from discord.ext import commands

client = commands.Bot(command_prefix = ".")

@client.event
async def on_ready():
    print("online")

@client.listen("on_message")
async def on_message(message):
    splited_message = message.content.split()
    guilds = []
    for guild in client.guilds:
        guilds.append(guild.id)

    if message.author == client.user:
        return

    if message.guild == None:
        try:
            guild_id = int(splited_message[0], base=10)
            current_guild = client.get_guild(guild_id)
            if guild_id in guilds:
                found_modmail = False
                for category in current_guild.categories:
                    if category.name == "Modmail":
                        found_modmail = True
                        break

                if found_modmail:
                    channel_name = "{}s-mail".format(str(message.author).lower().replace("#", ""))
                    found_channel = False

                    for c in current_guild.channels:
                        if c.name == channel_name:
                            found_channel = True
                            break

                    if found_channel:
                        await message.author.send("You already have a mail channel created! Your message is being sent.")
                        mail = splited_message[1:]
                        message = " ".join(mail)
                        await discord.utils.get(current_guild.channels, name=channel_name).send(message)
                    else:
                        await message.author.send("We are going to create a channel for your mail then send your message.")
                        await current_guild.create_text_channel(channel_name, category = discord.utils.get(current_guild.categories, name = "Modmail"))
                        mail = splited_message[1:]
                        header = message.author.mention + " asks: "
                        message = " ".join(mail)
                        await discord.utils.get(current_guild.channels, name = channel_name).send(header + message)
                else:
                    await message.author.send("The guild id is was valid however, there is no category for your mail yet. Please contact someone with administrative permissions to fix this.")
        except:
            pass

    elif message.guild != None:
        if str(discord.utils.get(message.guild.categories, id = message.channel.category_id)) == "Modmail":
            content_list = []

            async for msg in message.channel.history(limit=None):
                content_list.append(msg.content)

            first_message = content_list[-1]
            userid = int(first_message.split()[0].replace("<@", "").replace(">", ""))
            user = await client.fetch_user(userid)
            await user.send("".join(content_list[0]))


@commands.has_permissions(administrator=True)
@client.command()
async def setup(ctx, *args):
    roles = str(args)

    if (discord.utils.get(ctx.guild.categories, name = "Modmail") == None):
        for c in roles:
            character_ascii = ord(c)
            if character_ascii != 62 and (character_ascii < 48 or character_ascii > 57):
                roles = roles.replace(c, "")

        roles = roles.split(">")[:-1]

        for i in range(len(roles)):
            roles[i] = int(roles[i])

        if not roles:
            await ctx.send("Please give the names of the roles that should be able to see the mailbox.")
        else:
            category = await ctx.guild.create_category("Modmail")
            await category.set_permissions(ctx.guild.default_role, read_messages=False, send_messages=False)
            for role_id in roles:
                print(role_id)
                await category.set_permissions(discord.utils.get(ctx.guild.roles, id = role_id), read_messages=True, send_messages=True)
    else:
        await ctx.send("No need for setup! Modmail category already created!")

client.run("token")
