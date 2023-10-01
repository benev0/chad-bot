#import discord.py
import discord
from discord.ext import commands
#import psotgres driver
import psycopg2

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.typing = False
intents.presences = False

client = commands.Bot(command_prefix='$', intents=intents)

with open("secrets/psqluser") as f:
    conn = psycopg2.connect(
        dbname=f.readline().strip(),
        user=f.readline().strip(),
        password=f.readline().strip(),
        host=f.readline().strip(),
        port=f.readline().strip()
    )

class NoPrivateMessages(commands.CheckFailure):
    pass

class NotAdmin(commands.CheckFailure):
    pass

def get_expected(id: int):
    with conn.cursor() as cur:
        cur.execute(f"SELECT NAME FROM allowed_names WHERE id = {id};")
        return cur.fetchone()

@client.event
async def on_member_update(before, after):
    expected = get_expected(after.id);
    print(expected)
    if expected in after.display_name:
        print("username ok")
        return
    print(after.display_name)
    print(len(after.display_name))

@client.command()
async def status(ctx):
    await ctx.send('I am online!!')
    print(type(ctx.author.id))

@client.command()
async def name(ctx, member: discord.Member, nick):
    print("name recieved")
    await member.edit(nick=nick)
    await ctx.send(f"{member} aka {nick}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await client.process_commands(message)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


with open("secrets/token") as tFile:
    token = tFile.readline()
client.run(token)
