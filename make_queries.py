def check_dictator(ctx):
  roles = set(ctx.message.author.roles)
  print(roles)
  if "Bingo Dictator" in roles :
    return True
  else: 
    return False