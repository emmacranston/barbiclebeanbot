import discord
from discord.ext import commands
import psycopg2
import os

client = commands.Bot(command_prefix=".")
token = os.getenv("TOKEN")
db = os.getenv("DATABASE_URL")

@client.event
async def on_ready() :
    await client.change_presence(status = discord.Status.idle, activity = discord.Game("Listening to .help"))
    print("I am online")

@client.command()
async def ping(ctx) :
    await ctx.send(f"🏓 Pong with {str(round(client.latency, 2))}")

@client.command(name="whoami")
async def whoami(ctx) :
    await ctx.send(f"You are {ctx.message.author.name}")

@client.command()
async def clear(ctx, amount=3) :
    await ctx.channel.purge(limit=amount)

@client.command(name="bingolist")
def list_bingo_options():
  query_sql = "SELECT DISTINCT key FROM public.bingolist;"

  try: 
    print("connecting to database")
    conn = psycopg2.connect(db, sslmode='require')
    cursor = conn.cursor()
    cursor.execute(query_sql)
    records = cursor.fetchall()
    print("database connected")
    record_list = []
    record_string = ""
    for row in records:
      print(row)
      record_list.append(row)
      record_string.join(row + '\n')
    print("rows retrieved")
    print(f"(log) Bingo list includes... {record_string}")
    return(f"Bingo list includes... {record_string}")

  except:
    return "Error connecting to database"

  finally:
    if(conn):
      cursor.close()
      conn.close()
      print("cursor closed")

async def bingolist(ctx) :
  # await ctx.send("This is the current full list of Bingo card options.")
    bo = list_bingo_options()
    await ctx.send(f"bo {bo}")

@client.command(name="bingoadd")
async def bingoadd(ctx, item) :
    await ctx.send(f"Adding {item} to bingolist.")

client.run(token)