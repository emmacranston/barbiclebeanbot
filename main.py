import discord
from discord.ext import commands
from cogs import QueryEngine, Bingo
import psycopg2
import os

client = commands.Bot(command_prefix=".")
token = os.getenv("TOKEN")
db = os.getenv("DATABASE_URL")

def check_role(ctx):
  role = discord.utils.get(ctx.guild.roles, name="Bingo Dictator")
  if role in ctx.author.roles:
    return True
  else:
    return False

@client.event
async def on_ready() :
  await client.change_presence(status = discord.Status.idle
      , activity = discord.Game("Listening to .help")
    )
  print("I am online")
  try:
    client.load_extension('cogs.QueryEngine')
    print("Loaded extension '{0}'".format('QueryEngine'))
  except Exception as e:
    exc = '{0}: {1}'.format(type(e).__name__, e)
    print('Failed to load extension {0}\nError: {1}'.format('QueryEngine', exc))

  try: 
    client.load_extension('cogs.VoiceChannel')
    print("Loaded extension '{0}'".format('VoiceChannel'))
  except Exception as e:
      exc = '{0}: {1}'.format(type(e).__name__, e)
      print('Failed to load extension {0}\nError: {1}'.format('VoiceChannel', exc))



@client.command(name="startBingo", aliases=['sb'])
async def start_bingo(ctx) :
  """Starts up the bingo engine. Vroom vroom."""
  try:
    client.load_extension('cogs.Bingo')
    print("Loaded extension '{0}'".format('Bingo'))
  except Exception as e:
    exc = '{0}: {1}'.format(type(e).__name__, e)
    print('Failed to load extension {0}\nError: {1}'.format('Bingo', exc))

client.run(token)