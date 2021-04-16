def pull_bingolist():
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
        record_string += row[0] + "\n"
      print("rows retrieved")
      print(f"(log) Bingo list includes... {record_string}")
      await ctx.send(f"**Bingo list includes:** \n ```{record_string}```")


    except:
      print("Error connecting to database")

    finally:
      if(conn):
        cursor.close()
        conn.close()
        print("cursor closed")