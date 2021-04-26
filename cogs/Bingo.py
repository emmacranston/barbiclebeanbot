import discord
from discord.ext import commands
import os

class Bingo(commands.Cog):
	def __init__(self, client):
		self.client = client

		@commands.command(name='bl', aliases=["bingolist","BingoList","bl"])
		async def bl(self, ctx) :
		    """Lists the items used in this bingo game's card generator."""
		    print(ctx.guild.name)
		    query_sql = f"""
		    SELECT DISTINCT key 
		    FROM public.bingolist
		    WHERE server = '{ctx.guild.name}'
		    ;"""

		    listQuery = self.pull_query(query_sql,
		      ' ')
		    print(listQuery)
		    await ctx.send(f"**Bingo list includes:** ```\n{listQuery}```")
		 
		@commands.command(name='ping', aliases=['p'])
		async def ping(self, ctx):
			await ctx.send("Pong! :ping_pong:")

	def pull_query(self, query_sql, success_msg="Success", fail_msg="Failed"):
	  try:
	    print("connecting to database")
	    conn = psycopg2.connect(db, sslmode='require')
	    print("database connected")
	    cursor = conn.cursor()
	    cursor.execute(query_sql)
	    print("query executing")
	    records = cursor.fetchall()
	    print(records)
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
def setup(client):
	client.add_cog(Bingo(client))