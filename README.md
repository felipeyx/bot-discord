# 🤖 Discord Bot Multifuncional

Um bot de Discord completo com **comandos de música, jogos, utilitários e diversão**!  
Desenvolvido em **Python** utilizando `discord.py` e `yt_dlp` para reprodução de música do YouTube.

---

## ⚡ Funcionalidades

### 🎤 Música
- `!entrar` - Faz o bot entrar no canal de voz  
- `!sair` - Faz o bot sair do canal de voz  
- `!tocar <url>` - Toca uma música do YouTube  
- `!skip` - Pula a música atual  
- `!parar` - Para a música e desconecta  
- `!playrandom` - Toca uma música aleatória no canal de voz  

### 🧠 Jogos e Diversão
- `!adivinhar <número>` - Tente adivinhar um número de 1 a 10  
- `!gato` - Envia uma imagem aleatória de gato  
- `!cachorro` - Envia uma imagem aleatória de cachorro  
- `!gif` - Envia um GIF aleatório  
- `!meme` - Envia um meme aleatório  
- `!motivacao` - Envia uma frase motivacional  
- `!musica` - Sugere uma música aleatória  
- `!filmes` - Sugere 3 filmes aleatórios  
- `!contagem <número>` - Faz uma contagem regressiva  

### 📊 Utilitários
- `!imc <peso> <altura>` - Calcula seu Índice de Massa Corporal (IMC)  
- `!enquete <opção1> <opção2>` - Cria uma enquete simples  
- `!senha` - Gera uma senha aleatória  
- `!contar <frase>` - Conta quantas palavras tem na frase  

---

## 💻 Tecnologias
- **Python 3.10+**  
- **discord.py**  
- **yt_dlp**  
- **FFmpeg**  


---

## 🚀 Como executar

1. Instale Python 3.10+ e FFmpeg.
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Crie o bot no Discord Developer Portal e defina o token em uma variável de ambiente. **Nunca publique o token no repositório.**

Linux/macOS:

```bash
export DISCORD_TOKEN="seu-token"
export DISCORD_CHANNEL_ID="123456789012345678" # opcional
python bot.py
```

PowerShell:

```powershell
$env:DISCORD_TOKEN="seu-token"
$env:DISCORD_CHANNEL_ID="123456789012345678" # opcional
python bot.py
```

A variável `DISCORD_CHANNEL_ID` é opcional e define o canal que recebe a mensagem de inicialização.
