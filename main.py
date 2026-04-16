import discord
from discord.ext import commands
import datetime
import os

# === НАСТРОЙКИ ===
TOKEN = os.getenv('TOKEN')
# Цвет полоски в сообщениях (черный, как ты просил)
EMBED_COLOR = 0x010101

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'✅ Админ-бот {bot.user} запущен и готов раздавать люлей!')


# --- КОМАНДА: ОЧИСТКА ЧАТА ---
@bot.command(name='clear')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f'🗑️ Удалено **{amount}** сообщений.', delete_after=5)


# --- КОМАНДА: БАН ---
@bot.command(name='ban')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Причина не указана"):
    await member.ban(reason=reason)
    emb = discord.Embed(title="🔨 Бан", description=f"Пользователь {member.mention} был забанен.\n**Причина:** {reason}",
                        color=EMBED_COLOR)
    await ctx.send(embed=emb)


# --- КОМАНДА: МУТ (TIMEOUT) ---
@bot.command(name='мут')
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, time: str, *, reason="Причина не указана"):
    # Парсим время (например: 20мин, 1час, 1д)
    time_unit = time[-3:].lower()
    try:
        if "мин" in time:
            minutes = int(time.replace("мин", ""))
            duration = datetime.timedelta(minutes=minutes)
        elif "час" in time:
            hours = int(time.replace("час", ""))
            duration = datetime.timedelta(hours=hours)
        elif "д" in time:
            days = int(time.replace("д", ""))
            duration = datetime.timedelta(days=days)
        else:
            await ctx.send("❌ Укажите время правильно (например: 20мин, 1час, 2д)")
            return
    except ValueError:
        await ctx.send("❌ Ошибка в формате времени.")
        return

    await member.timeout(duration, reason=reason)
    emb = discord.Embed(title="🔇 Мут",
                        description=f"{member.mention} отправлен в угол на **{time}**.\n**Причина:** {reason}",
                        color=EMBED_COLOR)
    await ctx.send(embed=emb)


# --- КОМАНДА: INFO ---
@bot.command(name='info')
async def info(ctx, member: discord.Member = None):
    member = member or ctx.author
    roles = [role.mention for role in member.roles[1:]]  # Исключаем @everyone

    emb = discord.Embed(title=f"Информация о пользователе {member.name}", color=EMBED_COLOR)
    emb.set_thumbnail(url=member.display_avatar.url)
    emb.add_field(name="ID:", value=member.id, inline=True)
    emb.add_field(name="Никнейм:", value=member.display_name, inline=True)
    emb.add_field(name="Аккаунт создан:", value=member.created_at.strftime("%d.%m.%Y"), inline=False)
    emb.add_field(name="Зашел на сервер:", value=member.joined_at.strftime("%d.%m.%Y"), inline=False)
    emb.add_field(name=f"Роли ({len(roles)}):", value=" ".join(roles) if roles else "Нет ролей", inline=False)

    await ctx.send(embed=emb)


# --- КОМАНДА: KICK ---
@bot.command(name='kick')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="Причина не указана"):
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member.mention} был кикнут. Причина: {reason}")


# --- ОБРАБОТКА ОШИБОК (если нет прав) ---
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Бро, у тебя недостаточно прав для этой команды!")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("❌ Не могу найти этого челика.")


bot.run(TOKEN)
