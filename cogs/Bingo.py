import discord
from discord.ext import commands
import os

class Bingo(commands.Cog):
	def __init__(self, client):
		self.client = client

		@commands.command(name="bl")
		async def bl(ctx) :
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

def setup(client):
	client.add_cog(Bingo(client))