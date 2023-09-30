import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.typing = False
intents.presences = False

client = commands.Bot(command_prefix='$', intents=intents)

allow = {}

class NoPrivateMessages(commands.CheckFailure):
    pass

class NotAdmin(commands.CheckFailure):
    pass

def get_expected():
    pass

def check_username(user):
    return get_expected(user.id) == user.display_name;


@client.event
async def on_member_update(before, after):
    if not check_username(after.display_name):
        return

@client.command()
async def status(ctx):
    await ctx.send('I am online!!')

@client.command()
async def name(ctx, user, nick):
    pass


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await client.process_commands(message)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

if __name__ == '__main__':

    with open("token") as tFile:
        token = tFile.readline()
    client.run(token)
