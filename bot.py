import discord
import random
import datetime
import asyncio
import yt_dlp as youtube_dl
from discord.ext import commands

# Configuração do bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Configuração do youtube_dl
youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
}
ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

# Mensagem ao iniciar
@bot.event
async def on_ready():
    canal = bot.get_channel(1307068973614891130)  # Substituir pelo ID do canal
    if canal:
        await canal.send("🤖 Bot está online! Use `!ajuda` para ver os comandos disponíveis.")
    print(f"✅ {bot.user} está online!")

# Configuração do bot (comando de ajuda desativado)
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# 📜 Comando de ajuda personalizado
@bot.command(name="help", help="📜 Mostra a lista de comandos disponíveis")
async def help(ctx):
    embed = discord.Embed(
        title="📜 Lista de Comandos",
        description="Aqui estão todos os comandos disponíveis no bot.",
        color=discord.Color.blue()
    )

    comandos = {
        "🎤 Voz": {
            "!entrar": "Faz o bot entrar no canal de voz",
            "!sair": "Faz o bot sair do canal de voz",
            "!tocar <url>": "Toca uma música do YouTube",
            "!skip": "Pula a música atual",
            "!parar": "Para a música e desconecta",
            "!playrandom": "Toca um áudio aleatório no canal"
        },
        "🎮 Diversão": {
            "!adivinhar <número>": "Tente adivinhar um número de 1 a 10",
            "!gato": "Envia uma imagem aleatória de gato",
            "!cachorro": "Envia uma imagem aleatória de cachorro",
            "!gif": "Envia um GIF aleatório",
            "!meme": "Envia um meme aleatório",
            "!motivacao": "Envia uma frase motivacional",
            "!musica": "Sugere uma música aleatória",
            "!filmes": "Sugere 3 filmes aleatórios",
            "!contagem <número>": "Faz uma contagem regressiva"
        },
        "📊 Utilitários": {
            "!imc <peso> <altura>": "Calcula seu Índice de Massa Corporal (IMC)",
            "!enquete <opção1> <opção2>": "Cria uma enquete simples",
            "!senha": "Gera uma senha aleatória",
            "!contar <frase>": "Conta quantas palavras tem na frase"
        }
    }

    for categoria, comandos_lista in comandos.items():
        comandos_texto = "\n".join([f"**{cmd}** - {desc}" for cmd, desc in comandos_lista.items()])
        embed.add_field(name=categoria, value=comandos_texto, inline=False)

    embed.set_footer(text="Digite !help <comando> para mais detalhes.")
    
    await ctx.send(embed=embed)

# 🎤 1. Entrar no canal de voz
@bot.command(name="entrar", help="🎤 Faz o bot entrar no canal de voz")
async def entrar(ctx):
    if ctx.author.voice:
        canal = ctx.author.voice.channel
        await canal.connect()
        await ctx.send(f"🎤 Entrei no canal de voz: {canal}")
    else:
        await ctx.send("Você precisa estar em um canal de voz!")

# 🚪 2. Sair do canal de voz
@bot.command(name="sair", help="🚪 Faz o bot sair do canal de voz")
async def sair(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("🚪 Saí do canal de voz!")
    else:
        await ctx.send("Não estou em nenhum canal de voz.")

# 🎵 3. Tocar música
@bot.command(name="tocar", help="🎵 Toca uma música do YouTube")
async def tocar(ctx, url: str):
    if not ctx.voice_client:
        await ctx.invoke(entrar)

    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
    song_url = data['url']

    ctx.voice_client.stop()
    ffmpeg_audio = discord.FFmpegPCMAudio(song_url, **ffmpeg_options)
    ctx.voice_client.play(discord.PCMVolumeTransformer(ffmpeg_audio, volume=0.5))

    await ctx.send(f"🎵 Tocando agora: **{data['title']}**")

# ⏭️ 4. Pular música
@bot.command(name="skip", help="⏭️ Pula a música atual")
async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏩ Música pulada!")
    else:
        await ctx.send("❌ Não estou tocando nada!")

# ⏹️ 5. Parar música
@bot.command(name="parar", help="⏹️ Para a música e desconecta")
async def parar(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()
        await ctx.send("⏹️ Música parada e desconectado!")
    else:
        await ctx.send("❌ Não estou tocando nada!")

# 🧠 6. Jogo de adivinhação
@bot.command(name="adivinhar", help="🧠 Tente adivinhar um número de 1 a 10")
async def adivinhar(ctx, numero: int):
    certo = random.randint(1, 10)
    if numero == certo:
        await ctx.send("🎉 Parabéns! Você acertou!")
    else:
        await ctx.send(f"❌ Errou! O número era {certo}.")

# 💪 7. Calcular IMC
@bot.command(name="imc", help="💪 Calcula seu Índice de Massa Corporal (IMC)")
async def imc(ctx, peso: float, altura: float):
    resultado = peso / (altura ** 2)
    await ctx.send(f"📏 Seu IMC é {resultado:.2f}")

# 📊 8. Criar enquete
@bot.command(name="enquete", help="📊 Cria uma enquete simples")
async def enquete(ctx, opcao1: str, opcao2: str):
    mensagem = await ctx.send(f"📊 Enquete:\n1️⃣ {opcao1}\n2️⃣ {opcao2}")
    await mensagem.add_reaction("1️⃣")
    await mensagem.add_reaction("2️⃣")

# 🐱 9. Gato aleatório
@bot.command(name="gato", help="🐱 Envia uma imagem aleatória de gato")
async def gato(ctx):
    imagens = ["https://cataas.com/cat", "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExYjBtbDg1bTAxaGR0YjEzaTRlZHZsd2p2aWVhMmhmMm1ydmQxanBwaSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/KTnBZB1CsqMOQ/giphy.gif"]
    await ctx.send(random.choice(imagens))

# 🐶 10. Cachorro aleatório
@bot.command(name="cachorro", help="🐶 Envia uma imagem aleatória de cachorro")
async def cachorro(ctx):
    imagens = ["https://random.dog/woof.jpg", "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExM29jaGhya3k3YWt3MjU5d2EycGtlbHYzeXpsbmhwYTNhYWl6ajB0cCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/k1Psl92gw7YPSPYFKm/giphy.gif"]
    await ctx.send(random.choice(imagens))

    # 🎭 11. GIF aleatório
@bot.command(name="gif", help="🎭 Envia um GIF aleatório")
async def gif(ctx):
    gifs = [
        "https://media1.giphy.com/media/MDJ9IbxxvDUQM/giphy.gif",
        "https://media3.giphy.com/media/3o7aCYDNm1kXgSUgXm/giphy.gif",
        "https://media4.giphy.com/media/CAYVZA5NRb529kKQUc/giphy.gif"
    ]
    await ctx.send(random.choice(gifs))

# 🔐 12. Gerar senha aleatória
@bot.command(name="senha", help="🔐 Gera uma senha aleatória")
async def senha(ctx):
    caracteres = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%&*"
    senha = ''.join(random.choice(caracteres) for _ in range(10))
    await ctx.send(f"🔐 Sua senha gerada: `{senha}`")

  # 🎤 13. Contar palavras
@bot.command(name="contar", help="🎤 Conta quantas palavras tem na frase")
async def contar(ctx, *, frase: str):
    quantidade = len(frase.split())
    await ctx.send(f"📝 Sua frase tem {quantidade} palavras!")

    # 😂 14. Meme aleatório
@bot.command(name="meme", help="😂 Envia um meme aleatório")
async def meme(ctx):
    memes = [
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExazdpZXZiM2dpeXBwYmNqMnNqdnk3cWxoamF5NTM4amlqeTgybm52dSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/kd9BlRovbPOykLBMqX/giphy.gif",
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExMDR4dm10Y2R3OHlzN3hpMnF6cGZkYTNmcW96OWV5aHBhZWNrMDh3MiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/GeimqsH0TLDt4tScGw/giphy.gif",
        "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExdThyY2k2YzVrdzBvMzdqZ3Nkc25ubGVqZGNiYXNicG9yeTU1ejdiNSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/QMHoU66sBXqqLqYvGO/giphy.gif"
    ]
    await ctx.send(random.choice(memes))

    # 📢 15. Motivação
@bot.command(name="motivacao", help="📢 Envia uma frase motivacional")
async def motivacao(ctx):
    frases = [
        "O sucesso nasce do querer, da determinação e persistência!",
        "Nunca é tarde para ser quem você poderia ter sido!",
        "Se você pode sonhar, você pode realizar!"
    ]
    await ctx.send(random.choice(frases))

# 🎶 16. Sugestão de música
@bot.command(name="musica", help="🎶 Sugere uma música aleatória")
async def musica(ctx):
    musicas = [
        "Imagine Dragons - Believer",
        "Queen - Bohemian Rhapsody",
        "Linkin Park - In The End"
    ]
    await ctx.send(f"🎶 Sugestão de música: {random.choice(musicas)}")

    # 🎬 17. Sugestão de filmes
@bot.command(name="filmes", help="🎬 Sugere 3 filmes aleatórios")
async def filmes(ctx):
    filmes = ["Matrix", "O Poderoso Chefão", "Vingadores: Ultimato", "Interestelar", "Titanic"]
    await ctx.send(f"🎬 Recomendo esses filmes: {random.sample(filmes, 3)}")

# 🚀 18. Contagem regressiva
@bot.command(name="contagem", help="🚀 Faz uma contagem regressiva")
async def contagem(ctx, numero: int):
    if numero > 10:
        await ctx.send("🚨 Só posso contar até 10!")
        return
    for i in range(numero, 0, -1):
        await ctx.send(f"{i}...")
        await asyncio.sleep(1)
    await ctx.send("🎉 BOOM!")

    # 🎶 19. Tocar áudio aleatório
@bot.command(name="playrandom", help="🎶 Toca um áudio aleatório no canal de voz")
async def playrandom(ctx):
    if not ctx.voice_client:
        await ctx.invoke(entrar)  # Faz o bot entrar no canal de voz se ainda não estiver

    url = random.choice([
        "https://www.youtube.com/watch?v=_P5vR9pz5Hc",
        "https://www.youtube.com/watch?v=S06IYs3csWI",
        "https://www.youtube.com/watch?v=FJZIl0JPmgs"
    ])  # Escolhe uma música aleatória 🎵

    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
    song_url = data['url']

    ctx.voice_client.stop()
    ffmpeg_audio = discord.FFmpegPCMAudio(song_url, **ffmpeg_options)
    ctx.voice_client.play(discord.PCMVolumeTransformer(ffmpeg_audio, volume=0.5))

    await ctx.send(f"🎵 Tocando agora: **{data['title']}**")

# Iniciar o bot
bot.run("ID BOT")