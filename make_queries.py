def check_dictator(ctx):
  roles = set(ctx.message.author.roles)
  if "Bingo Dictator" in roles :
    return True
  else: 
    return False