import psycopg2
import discord
from discord.ext import commands
import os

class QueryEngine(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.db = os.getenv("DATABASE_URL")
	def pull_query(self, query_sql, success_msg="Success", fail_msg="Failed"):
	  try:
	    print("connecting to database")
	    conn = psycopg2.connect(self.db, sslmode='require')
	    print("database connected")
	    cursor = conn.cursor()
	    cursor.execute(query_sql)
	    print("query executing")
	    records = cursor.fetchall()
	    record_string = ""
	    for row in records:
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
def setup(client):
	client.add_cog(QueryEngine(client))

