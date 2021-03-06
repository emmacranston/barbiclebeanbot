# VoiceChannel
import os
import discord
from discord.ext import commands


class VoiceChannel(commands.Cog):
	"""Voice channel commands"""

	def __init__(self, client):
		self.client = client
		self.catname = "Voice Channels"
		self.vcname = "Focus Time"

	@commands.command(name = 'vc')
	async def vc(self, ctx):
		"""Begins a voice chat channel. Type vc [category, channel name] to create a voice chat channel with the listed name in the listed category."""
		content = ctx.message.content.split(".vc")[-1]
		if len(content) > 0:
			self.catname = content.split(",")[0]
			self.vcname = content.split(",")[1]
		await ctx.send(f"Creating voice channel {self.vcname} in category {self.catname}")
		cat = discord.utils.get(guild.categories, name=self.catname)
		await ctx.guild.create_voice_channel(self.vcname,
			category = cat)

	@commands.command(name='kvc')
	async def kvc(self, ctx) :
		"""Kills a voice chat channel."""
		content = ctx.message.content.split(".kvc ")[-1]
		print(content)
		try:
			ch = discord.utils.get(guild.voice_channels, name=content)
			print(ch.name)
			await ch.delete()
			await ctx.send(f"Channel {content} deleted")
		except Exception as e:
			await ctx.send(f"Channel {content} not deleted; see logs.")
			print("Channel {0} not deleted: {1}".format(content, e))

	@commands.command(name='muteall')
	async def muteall(self, ctx) :
		"""Sets voice channel permissions to mute everybody."""
		content = ctx.message.content.split(".muteall")[-1]
		if len(content) > 0:
			cat = content.split(" ")[0]
			vcname = content.split(" ")[1]
		else: 
			cat = self.cat
			vcname = self.vcname
		try: 
			for vc in ctx.guild.voice_channels:
				if vc.name == vcname:
					for member in vc.members:
						await vc.set_permissions(speak = False)
		except Exception as e:
			print("No voice chat in category {0} is named {1}".format(cat, vcname))

def setup(client):
	client.add_cog(VoiceChannel(client))
