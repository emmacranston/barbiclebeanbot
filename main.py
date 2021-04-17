import discord
from discord.ext import commands
import psycopg2
import os

from make_queries import check_dictator

client = commands.Bot(command_prefix=".")
token = os.getenv("TOKEN")
db = os.getenv("DATABASE_URL")

@client.event
async def on_ready() :
    await client.change_presence(status = discord.Status.idle, activity = discord.Game("Listening to .help"))
    print("I am online")

# @client.command()
# async def ping(ctx) :
#     await ctx.send(f"🏓 Pong with {str(round(client.latency, 2))}")

# @client.command(name="whoami")
# async def whoami(ctx) :
#     await ctx.send(f"You are {ctx.message.author.name}")

# @client.command()
# async def clear(ctx, amount=3) :
#     await ctx.channel.purge(limit=amount)

@client.command(name="bingolist")
async def bingolist(ctx) :
    """Lists the items used in this bingo game's card generator."""
    print(ctx.guild.name)
    query_sql = f"""
    SELECT DISTINCT key 
    FROM public.bingolist
    WHERE server = '{ctx.guild.name}'
    ;"""

    try: 
      print("connecting to database")
      conn = psycopg2.connect(db, sslmode='require')
      cursor = conn.cursor()
      cursor.execute(query_sql)
      records = cursor.fetchall()
      print("database connected")
      record_string = ""
      for row in records:
        print(row)
        record_string += row[0] + "\n"
      print("rows retrieved")
      print(f"(log) Bingo list includes... {record_string}")
      await ctx.send(f"**Bingo list includes:** ```\n{record_string}```")

    except:
      print("Error connecting to database")

    finally:
      if(conn):
        cursor.close()
        conn.close()
        print("cursor closed")

@client.command(name="bingoadd")
async def bingoadd(ctx) :
    """ Adds an item to the bingo list.
     #TODO 
     * add game czar check before bingo is added
     * and a sarcastic message if non-bingo czar tries it ("Nice try, PEASANT!")
    """
    print(ctx.guild.name)
    item = ctx.message.content
    query_sql = f"""INSERT INTO public.bingolist (key, server)
    VALUES ('{item}', '{ctx.guild.name}' )"""
    try:
      print("connecting to database")
      conn = psycopg2.connect(db, sslmode='require')
      cursor = conn.cursor()
      cursor.execute(query_sql)
      conn.commit()
      await ctx.send(f"Added {item} to bingolist.")
    except psycopg2.errors.UniqueViolation:
      await ctx.send(f"{item} is already in the bingo list!")
    except:
      await ctx.send("Error inserting value to database")
    finally:
      if(conn):
        cursor.close()
        conn.close()
        await ctx.send("Cursor Closed")

@client.command(name="found")
async def found(ctx):
  # TODO: make sure the item name is in the card items list
    await ctx.send(f"You said: {ctx.message.content}")
    msg = ctx.message.content.split(',')
    key = msg[0]
    link = msg[1]
    print(ctx.guild.name)
    query_sql = f"""INSERT INTO public.current_game (bingo_key, link)
    VALUES ('{key}', '{link}');"""
    try:
      print("connecting to database")
      conn = psycopg2.connect(db, sslmode='require')
      cursor = conn.cursor()
      cursor.execute(query_sql)
      conn.commit()
      await ctx.send(f"Added {key} with link {link} to current game.")
    except psycopg2.errors.UniqueViolation:
      await ctx.send(f"{key} has already been found!")
    except:
      await ctx.send("Error inserting value to database")
    finally:
      if(conn):
        cursor.close()
        conn.close()
        print("Cursor Closed")

# @client.command(name="run_query")
# async def run_query(sql, msg, error_msg=''):
#   try:
#       print("connecting to database")
#       conn = psycopg2.connect(db, sslmode='require')
#       cursor = conn.cursor()
#       cursor.execute(sql)
#       conn.commit()
#       await ctx.send("msg")
#   except psycopg2.errors.UniqueViolation:
#     await ctx.send(error_msg)
#   except:
#     await ctx.send("Error inserting value to database")
#     print("Query failed")
#   finally:
#     if(conn):
#       cursor.close()
#       conn.close()
#       print("Cursor Closed")

# @client.command(name='find')
# async def find(ctx):
#     msg = ctx.message.content.split(',')
#     key = msg[0]
#     link = msg[1]
#     print(ctx.guild.name)
#     query_sql = f"""INSERT INTO public.current_game (bingo_key, link)
#     VALUES ('{key}', '{link}');"""

#     print(f"Attempting query {query_sql}")
#     await ctx.invoke(bot.get_command('run_query'), query=query_sql)

@client.command(name="newgame")
async def newGame(ctx):
  """ Makes a new game. If you're the Bingo Dictator.
  #TODO 
   * check that the user is game czar
   * swap public.current_list with public.prior_list
   * make a new blank list in public.current_list out of the available entries in bingolist
      * link and confirmation will be blank
   * make a new game in public.current_game, wipe old players list to public.last_game
  """
  role = discord.utils.get(ctx.guild.roles, name="Bingo Dictator")
  if role in ctx.author.roles:
    await ctx.send(f"You are the Bingo Dictator with role {role.name}")
  else:
    await ctx.send("You are a PEASANT!")

@client.command(name="confirmfind")
async def confirmFind(ctx, item):
  """  Confirms that a 'found' item has been accepted.
  #TODO
   * update public.current_list to reflect confirmations from game czar
   * add sarcastic message if non-czar tries it
  """
  dictator = discord.utils.get(ctx.guild.roles, name="Bingo Dictator")
  if dictator in ctx.author.roles:
    
  else:
    await ctx.send("Simple _peasants_ mayn't confirm Bingo finds.")

@client.command(name="currentlist")
async def currentlist(ctx) :
    """ Shows the current list of items that have been confirmed by the Bingo Dictator.
    #TODO
     * add server protection check
    """
    query_sql = "SELECT * FROM public.current_game WHERE confirmed = TRUE;"
    try:
      conn = psycopg2.connect(db, sslmode='require')
      cursor = conn.cursor()
      cursor.execute(query_sql)
      records = cursor.fetchall()

      record_string = ''
      for row in records:
        rowvals = ''
        for item in row:
          rowvals += str(item) + ', '
          print(rowvals)
        record_string += rowvals + "\n"
      await ctx.send(f"All data: ```{record_string}```")

    except:
      print("Error connecting to database")

    finally:
      if(conn):
        cursor.close()
        conn.close()


client.run(token)