import discord
import random
import lavalink 
import os
from discord.ext import commands, tasks
from pathlib import Path
from random import choice

client = commands.Bot(command_prefix = '/')


@commands.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
async def hi(ctx, member):
    await ctx.send(f"Hello! {member}")

@client.command()
async def userinfo(ctx):
    user = ctx.author

    embed=discord.Embed(title="USER INFO", description=f"Here is the info we retrieved about {user}", colour=user.colour)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="NAME", value=user.name, inline=True)
    embed.add_field(name="NICKNAME", value=user.nick, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="STATUS", value=user.status, inline=True)
    embed.add_field(name="TOP ROLE", value=user.top_role.name, inline=True)
    await ctx.send(embed=embed)

@commands.Cog.listener()
async def on_member_join(member):
 print(f'{member} has joined the server.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left the server.')

@client.command(aliases=['purge'])
async def clear(ctx, count=1):
    await ctx.channel.purge(limit=count + 1)

@client.command()
async def sekks(ctx):
    await ctx.send("no sekks tonight #stayavirgin")

@client.command()
async def kick(ctx, usermention: discord.Member, *, reason):
    await usermention.kick()
    await ctx.send("The user got kicked")

@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
 await member.ban(reason=reason)

@client.command(description='Mutes the specified user.')
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *,reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name='Muted')
    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")
        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False)
    await member.add_roles(mutedRole, reason=reason)
    await ctx.send(f"Muted {member.mention} for reason {reason}")
    await member.send(f"You were muted in the server {guild.name} for {reason}")

@client.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx,member:discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name='Muted')
    await member.remove_roles(mutedRole)
    await ctx.send(f"Unmuted {member.mention}")
    #await member.send(f"You were unmuted in the server {guild.name} for {reason}")

@client.command()
async def unban(ctx, *, member):
    await ctx.send("yes")

#@client.command(aliases=['8ball'])
#async def eightball(ctx, *, questions):
#    responses = ["As I see it, yes", "Yes", "No", "Very likely", "Not even close", "Maybe", "Very unlikely", "Gino's mom told me yes", "Gino's mom told me no", "Ask again later", "Better not tell you now", "Concentrate and ask again", "Don't count on it", " It is certain", "My sources say no", "Outlook good", "You may rely on it", "Very Doubtful", "Without a doubt"]
#    await ctx.send('Question: {} \nAnswer: {} '.format(ctx.message.content.strip('/8ball '), random.choice(responses)))
    #await ctx.send(random.choice(possible_responses) + ", " + context.message.author.mention)


async def info(ctx, commandSent=None):
    if commandSent != None:

        for command in bot.commands:
            if commandSent.lower() == command.name.lower():

                paramString = ""

                for param in command.clean_params:
                    paramString += param + ", "

                paramString = paramString[:-2]

                if len(command.clean_params) == 0:
                    paramString = "None"
                   
                embed=discord.Embed(title=f"HELP - {command.name}", description=command.description)
                embed.add_field(name="parameters", value=paramString)
                await ctx.message.delete()
                await ctx.author.send(embed=embed)
       
    else:
        embed=discord.Embed(title="HELP")
        embed.add_field(name="ping", value="Gets the bots latency", inline=True)
        embed.add_field(name="hi", value="Says hello to a specified user, Parameters: Member", inline=True)
        embed.add_field(name="userinfo", value="Retreives info about the user", inline=True)
        embed.add_field(name="8ball", value="Ask a question, get a epic answer from 8ball!", inline=True)
        embed.add_field(name="sekks", value="Immature command created by the community of Swiss001", inline=True)
        embed.add_filed(name="Ban", value="Ban a certain user from the server",inline=True)
        embed.add_field(name="Kick",value="Kick a certain user from the server", inline=True)
        embed.add_field(name="unban",value="Unban a certain user from the server",inline=True)
        embed.add_field(name="Mute",value="Mute a certain user from speaking in the server",inline=True)
        embed.add_field(name="Unmute",value="Unmute a certain user",inline=True)
        embed.add_field(name="purge",value="Clear the chat",inline=True)
        await ctx.message.delete()
        await ctx.author.send(embed=embed)


class MusicBot(commands.Bot):
    def __init__(self):
        self._cogs = [p.stem for p in Path(".").glob("./bot/cogs/*.py")]
        super().__init__(command_prefix=self.prefix, case_insensitive=True)

    def setup(self):
        print("Running setup...")

        for cog in self._cogs:
            self.load_extension(f"bot.cogs.{cog}")
            print(f" Loaded `{cog}` cog.")

        print("Setup complete.")

    def run(self):
        self.setup()

        with open("data/token.0.txt", "r", encoding="utf-8") as f:
            TOKEN = f.read()

        print("Running bot...")
        super().run(TOKEN, reconnect=True)

    async def shutdown(self):
        print("Closing connection to Discord...")
        await super().close()

    async def close(self):
        print("Closing on keyboard interrupt...")
        await self.shutdown()

    async def on_connect(self):
        print(f" Connected to Discord (latency: {self.latency*1000:,.0f} ms).")

    async def on_resumed(self):
        print("Bot resumed.")

    async def on_disconnect(self):
        print("Bot disconnected.")

    # async def on_error(self, err, *args, **kwargs):
    #     raise

    # async def on_command_error(self, ctx, exc):
    #     raise getattr(exc, "original", exc)

    async def on_ready(self):
        self.client_id = (await self.application_info()).id
        print("Bot ready.")

    async def prefix(self, bot, msg):
        return commands.when_mentioned_or("/")(bot, msg)

    async def process_commands(self, msg):
        ctx = await self.get_context(msg, cls=commands.Context)

        if ctx.command is not None:
            await self.invoke(ctx)

    async def on_message(self, msg):
        if not msg.author.bot:
            await self.process_commands(msg)