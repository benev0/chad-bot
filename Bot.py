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

def guild():
    async def predicate(ctx):
        if ctx.guild is None:
            raise NoPrivateMessages('Hey no DMs!')
        return True
    return commands.check(predicate)

def admin():
    async def predicate(ctx):
        if not ctx.author.guild_permissions.administrator:
            raise NotAdmin(f'{ctx.author} are not elevated enough to execute this command')
        return True
    return commands.check(predicate)

def get_expected(id: int):
    with conn.cursor() as cur:
        cur.execute(f"SELECT NAME FROM allowed_names WHERE id = {id};")
        data = cur.fetchone()
        return data[0].strip() if data is not None else None

@client.event
async def on_member_update(before, after):
    print("updating")
    expected = get_expected(after.id);
    if expected is None:
        return
    if expected in after.display_name:
        return
    await after.edit(nick=expected)

@client.command()
@guild()
@admin()
async def name(ctx, member: discord.Member, nick):
    nickFormat = ''.join(nick.lower().split())[:32]
    with conn.cursor() as cur:
        cur.execute(
            f"""INSERT INTO allowed_names (id, name)
            VALUES ({member.id}, '{nickFormat}')
            ON CONFLICT (id)
            DO UPDATE
            SET name = EXCLUDED.name;"""
        )
    conn.commit()
    try:
        await on_member_update(member, member)
        await ctx.send(f"{member} aka {nickFormat}")
    except:
        await ctx.send(f"Bot Could not compleate transaction")

@client.command()
@guild()
@admin()
async def runall(ctx, role=None: discord.role):
    if role is not None and not ctx.guild.me.guild_permissions.manage_roles:
        await ctx.send('This bot does not have permission to manage roles')
    for member in ctx.guild.members:
        expected = get_expected(member.id)
        if expected is Null and role is not None:
            try:
                await member.add_roles(role)
        if expected in member.display_name:
            continue
        try:
            await on_member_update(member, member)

@client.command()
@guild()
@admin()
async def delete(ctx, member: discord.Member)
    with conn.cursor() as cur:
        cur.execute(f"DELETE FROM allowed_names WHERE id = {member.id}")
    conn.commit()

@client.command()
@guild()
async def whoami(ctx):
    await ctx.send(f'{get_expected(ctx.author.id)}')

@client.command()
@guild()
async def whois(ctx, member: discord.Member):
    await ctx.send(f'{get_expected(member.id)}')

@client.command()
async def status(ctx):
    await ctx.send('I am online!!')

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
