import os
import discord
from discord.ext import commands
import aiohttp
import io
#from dotenv import load_dotenv

#load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # Нужно для работы !cat

bot = commands.Bot(command_prefix='!', intents=intents)

class CatButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # чтобы кнопка не исчезала со временем

    @discord.ui.button(label="Show cat 🐱", style=discord.ButtonStyle.primary)
    async def send_cat(self, interaction: discord.Interaction, button: discord.ui.Button):
        url = 'https://cataas.com/cat'

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    image_data = await resp.read()
                    file = discord.File(io.BytesIO(image_data), filename="cat.jpg")
                    await interaction.response.send_message(
                        file=file,
                        view=CatButton()  # снова добавляем кнопку
                    )
                else:
                    await interaction.response.send_message("Could not get a cat 😿", ephemeral=True)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} is ready!')

@bot.command()
async def cat(ctx):
    await ctx.send("Here's a cat for you!", view=CatButton())

bot.run(TOKEN)
