import discord
from discord.ext import commands
from discord import app_commands
import datetime

intents = discord.Intents.default()
intents.message_content = True 
intents.members = True 

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self):
        await self.tree.sync()

bot = MyBot()

@bot.event
async def on_ready():
    print(f'Ботът {bot.user.name} е готов! 🚀')

@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel:
        await channel.send(f'Добре дошъл, {member.mention}! 🎉')

# --- ОСТАНАЛИ КОМАНДИ ---

@bot.tree.command(name="hello", description="Поздрав")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'Здравей, {interaction.user.name}!')

@bot.tree.command(name="joke", description="Виц")
async def joke(interaction: discord.Interaction):
    await interaction.response.send_message("Защо компютърът не спи? Защото има прозорци!")

@bot.tree.command(name="hack", description="Хакни някой (шега)")
async def hack(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(f'💻 Хакване на {member.name}... Парола: `123456` 🕵️')

@bot.tree.command(name="server", description="Инфо сървър")
async def server(interaction: discord.Interaction):
    await interaction.response.send_message(f'Сървър: {interaction.guild.name} | Хора: {interaction.guild.member_count}')

@bot.tree.command(name="userinfo", description="Инфо потребител")
async def userinfo(interaction: discord.Interaction, member: discord.Member = None):
    member = member or interaction.user
    await interaction.response.send_message(f'Име: {member.name}\nID: {member.id}')

@bot.tree.command(name="ping", description="Провери пинга")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'🏓 {round(bot.latency * 1000)}ms')

@bot.tree.command(name="clear", description="Изтриване")
@app_commands.checks.has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount: int):
    await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f'🧹 Изтрити {amount}', ephemeral=True)

@bot.tree.command(name="kick", description="Кик")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member):
    await member.kick()
    await interaction.response.send_message(f'👢 {member.name} изгонен.')

@bot.tree.command(name="ban", description="Бан")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member):
    await member.ban()
    await interaction.response.send_message(f'🔨 {member.name} баниран.')

@bot.tree.command(name="slowmode", description="Бавен режим")
@app_commands.checks.has_permissions(manage_channels=True)
async def slowmode(interaction: discord.Interaction, seconds: int):
    await interaction.channel.edit(slowmode_delay=seconds)
    await interaction.response.send_message(f'⏳ Бавен режим: {seconds}s')

@bot.tree.command(name="mute", description="Таймаут")
@app_commands.checks.has_permissions(moderate_members=True)
async def mute(interaction: discord.Interaction, member: discord.Member, minutes: int):
    duration = datetime.timedelta(minutes=minutes)
    await member.timeout(duration)
    await interaction.response.send_message(f'🤐 {member.name} заглушен за {minutes}м.')

bot.run('MTQ2OTQyODEwODc1ODA4OTc1OA.G0Xi4A.xe9nFPLtTZR2YsExX_aBiwbumH2x5xWP231QFo')
