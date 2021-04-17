import discord
from discord.ext import commands
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

def run_query(query_sql, success_msg='Success', fail_msg='Failed'):
  try:
    print("connecting to database")
    conn = psycopg2.connect(db, sslmode='require')
    cursor = conn.cursor()
    cursor.execute(query_sql)
    conn.commit()
    return success_msg
  except psycopg2.errors.UniqueViolation:
    return fail_msg
  except:
    return "Error inserting value to database"
  finally:
    if(conn):
      cursor.close()
      conn.close()

def pull_query(query_sql, success_msg="Success", fail_msg="Failed"):
  try:
    print("connecting to database")
    conn = psycopg2.connect(db, sslmode='require')
    print("database connected")
    cursor = conn.cursor()
    cursor.execute(query_sql)
    print("query executing")
    results = cursor.fetchall()
    print(results)
    record_string = ""
    for row in records:
      print(row)
      row_string = ""
      for value in row:
        row_string += value + ", "
      record_string += row_string + "\n"
      print(record_string)
    return success_msg + record_string

  except psycopg2.errors.UniqueViolation:
    return fail_msg
  except:
    return "Error pulling data."
  finally:
    if(conn):
      cursor.close()
      conn.close()

@client.event
async def on_ready() :
    await client.change_presence(status = discord.Status.idle, activity = discord.Game("Listening to .help"))
    print("I am online")

@client.command(name="BingoAdd")
async def BingoAdd(ctx) :
  """ Adds an item to the bingo list.
   #TODO 
   * add game czar check before bingo is added
   * and a sarcastic message if non-bingo czar tries it ("Nice try, PEASANT!")
  """
  content = ctx.message.content
  print(content)
  item = content.split(".bingoAdd ")[-1]
  print(item)
  query_sql = f"""INSERT INTO public.bingolist (key, server)
  VALUES ('{item}', '{ctx.guild.name}' )"""
  addQuery = run_query(query_sql
    , f"Added {item} to bingolist."
    , f"{item} is already in the bingo list."
    )
  await ctx.send(addQuery)

@client.command(name="bingolist")
async def bingolist(ctx) :
    """Lists the items used in this bingo game's card generator."""
    print(ctx.guild.name)
    query_sql = f"""
    SELECT DISTINCT key 
    FROM public.bingolist
    WHERE server = '{ctx.guild.name}'
    ;"""

    listQuery = pull_query(query_sql,
      ' ')
    print(listQuery)
    await ctx.send(f"**Bingo list includes:** ```\n{listQuery}```")

@client.command(name="currentlist")
async def currentlist(ctx) :
    """ Shows the current list of items that have been confirmed by the Bingo Dictator.
    #TODO
     * add server protection check
    """
    query_sql = "SELECT * FROM public.current_game WHERE confirmed = TRUE;"
    clistQuery = run_query(query_sql,
      f"All data: ```{record_string}```")
    await ctx.send(clistQuery)

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
    pass
  else:
    await ctx.send("Simple _peasants_ mayn't confirm Bingo finds.")


client.run(token)