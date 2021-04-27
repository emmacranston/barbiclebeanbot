import os
import discord
from discord.ext import commands

class Bingo(QueryEngine):
	"""Commands for a bingo game."""
	def __init__(self, client):
		self.client = client
		self.query_engine = self.client.get_cog('QueryEngine')

	@commands.command(name='bl', aliases=["bingolist","BingoList"])
	async def bl(self, ctx) :
	    """Lists the items used in this bingo game's card generator."""
	    print(ctx.guild.name)
	    query_sql = f"""
	    SELECT DISTINCT key 
	    FROM public.bingolist
	    WHERE server = '{ctx.guild.name}'
	    ;"""

	    listQuery = self.query_engine.pull_query(query_sql,
	      ' ')
	    print(listQuery)
	    await ctx.send(f"**Bingo list includes:** ```\n{listQuery}```")

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

	    foundQuery = run_query(query_sql,
	      f"Added {key} with link {link} to current game.",
	      f"{key} has already been found!"
	      )
	    await ctx.send(foundQuery)

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

	@client.command(name="joingame")
	async def joingame(ctx):
	  """Allows you to join a new game.
	  #TODO
	  """
	  pass

	@client.command(name="leavegame")
	async def leavegame(ctx):
	  """Allows you to leave the game.
	  """
	  pass
def setup(client):
	client.add_cog(QueryEngine)
	client.add_cog(Bingo(client))